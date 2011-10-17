#!/usr/bin/env python
# encoding: utf-8

###
# Copyright 2011 University of Warsaw, Krzysztof Rusek
# 
# This file is part of SegmEdit.
#
# SegmEdit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SegmEdit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SegmEdit.  If not, see <http://www.gnu.org/licenses/>.


import sqlite3
import os
import config
import re

conn = None
cur = None

def init():
    global conn, cur
    conn = sqlite3.connect(config.DATABASE_FILE)
    cur = conn.cursor()

    if not cur.execute('SELECT COUNT(*) FROM sqlite_master WHERE name = "articles"').fetchone()[0]:
        print 'Creating table articles'
        cur.execute("""
            CREATE TABLE articles (
                fileid   TEXT          PRIMARY KEY,
                title    TEXT NOT NULL,
                status   TEXT NOT NULL DEFAULT "unlocked",
                comment  TEXT NOT NULL DEFAULT "",
                username TEXT     NULL DEFAULT NULL
            );
        """)

xmls = set()

def findxmls():
    r = re.compile(r'^(.{8})\.xml$')
    for name in os.listdir(config.XMLS_DIR):
        m = r.match(name)
        if m:
            xmls.add(m.group(1))

pdfs = set()

def findpdfs():
    r = re.compile(r'^(.{8})\.pdf$')
    for name in os.listdir(config.PDFS_DIR):
        m = r.match(name)
        if m:
            pdfs.add(m.group(1))

docs = None

def insert():
    conn2 = sqlite3.connect('doaj.sqlite')
    cur2 = conn2.cursor()
    for doc in docs:
        if not cur.execute('SELECT COUNT(*) FROM articles WHERE fileid = ?', (doc,)).fetchone()[0]:
            row = cur2.execute('SELECT atitle FROM article WHERE fileid = ?', (doc,)).fetchone()
            if row:
                print 'Adding article %s with title "%s"' % (doc, row[0])
                cur.execute('INSERT INTO articles (fileid, title) VALUES (?, ?)', (doc, row[0]))
            else:
                print 'Could not find info for article %s' % doc

if __name__ == "__main__":
    init()
    findxmls()
    findpdfs()
    docs = xmls & pdfs
    for xml in xmls - pdfs:
        print 'Missing pdf file for xml "%s.xml"' % xml
    for pdf in pdfs - xmls:
        print 'Missing xml file for pdf "%s.pdf"' % pdf
    insert()
    conn.commit()
    conn.close()
