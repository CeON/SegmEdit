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
import sys
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


def print_help():
    print 'Usage:'
    print ''
    print '  %s help' % sys.argv[0]
    print '      -- prints this help'
    print ''
    print '  %s list' % sys.argv[0]
    print '      -- lists available articles'
    print ''
    print '  %s reset_db' % sys.argv[0]
    print '      -- cleans database of available articles (do not touch files)'
    print ''
    print '  %s sync_db' % sys.argv[0]
    print '      -- creates indexes to files existing in directories, sets generic titles.'
    print '         If you want to set a title, use the "add" command'
    print ''
    print '  %s add <fileid> [<title>]' % sys.argv[0]
    print '      -- adds into database info about an article'
    print ''
    print '  %s del <fileid>' % sys.argv[0]
    print '      -- deletes from database info abuot an article'
    print ''


def list_docs():
    for row in cur.execute('SELECT * FROM articles'):
        print row


def reset_db():
    print >> sys.stderr, 'Are you sure to delete ALL articles from database? [y,N] ',
    resp = raw_input()
    if resp in ('y', 'Y'):
        print 'Deleting articles from database (PDF and XML files are not touched)'
        cur.execute('DELETE FROM articles')


def sync_db():
    xmls = set()
    pdfs = set()
    docs = None

    # finding xmls
    r = re.compile(r'^(.{8})\.xml$')
    for name in os.listdir(config.XMLS_DIR):
        m = r.match(name)
        if m:
            xmls.add(m.group(1))
    
    # finding pdfs
    r = re.compile(r'^(.{8})\.pdf$')
    for name in os.listdir(config.PDFS_DIR):
        m = r.match(name)
        if m:
            pdfs.add(m.group(1))

    docs = xmls & pdfs

    for xml in xmls - pdfs:
        print >> sys.stderr, 'Missing pdf file for xml "%s.xml"' % xml
    for pdf in pdfs - xmls:
        print >> sys.stderr, 'Missing xml file for pdf "%s.pdf"' % pdf

    for doc in docs:
        if not cur.execute('SELECT COUNT(*) FROM articles WHERE fileid = ?', (doc,)).fetchone()[0]:
            print 'Adding article %s with title "%s"' % (doc, row[0])
            cur.execute('INSERT INTO articles (fileid, title) VALUES (?, ?)', (doc, 'Article ' + doc))


def add_article():
    if len(sys.argv) < 3:
        print >> sys.stderr, 'Missing article index (filename without extension)'
        exit(1)
    fileid = sys.argv[2]
    if len(sys.argv) > 3:
        title = sys.argv[3]
    else:
        title = 'Article ' + fileid

    if not os.path.isfile(config.XMLS_DIR + os.path.sep + fileid + '.xml'):
        print >> sys.stderr, 'Missing %s.xml file' % fileid
        exit(1)
    if not os.path.isfile(config.PDFS_DIR + os.path.sep + fileid + '.pdf'):
        print >> sys.stderr, 'Missing %s.pdf file' % fileid
        exit(1)

    if not cur.execute('SELECT COUNT(*) FROM articles WHERE fileid = ?', (fileid,)).fetchone()[0]:
        print 'Adding article %s with title "%s"' % (fileid, title)
        cur.execute('INSERT INTO articles (fileid, title) VALUES (?, ?)', (fileid, title))
    else:
        print >> sys.stderr, 'Article %s already in database' % fileid
        exit(1)


def del_article():
    if len(sys.argv) < 3:
        print >> sys.stderr, 'Missing article index (filename without extension)'
        exit(1)
    fileid = sys.argv[2]

    if cur.execute('SELECT COUNT(*) FROM articles WHERE fileid = ?', (fileid,)).fetchone()[0]:
        print >> sys.stderr, 'Are you sure to delete article %s from database? [y,N] ' % fileid, 
        resp = raw_input()
        if resp in ('y', 'Y'):
            print 'Deleting article %s from database (PDF and XML files are not touched)' % fileid
            cur.execute('DELETE FROM articles WHERE fileid = ?', (fileid,))
    else:
        print >> sys.stderr, 'Article %s not in database' % fileid
        exit(1)

if __name__ == "__main__":
    if len(sys.argv) <= 1 or sys.argv[1] == 'help':
        print_help()

    else:
        init()

        if sys.argv[1] == 'list':
            list_docs()
        elif sys.argv[1] == 'reset_db':
            reset_db()
        elif sys.argv[1] == 'sync_db':
            sync_db()
        elif sys.argv[1] == 'add':
            add_article()
        elif sys.argv[1] == 'del':
            del_article()
        else:
            print >> sys.stderr, 'Unknown argument: %s. Type "%s help" to see available options.' % (sys.argv[1], sys.argv[0])

        conn.commit()
        conn.close()
