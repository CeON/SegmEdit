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
import config

def isAdmin(username):
    return username in config.ADMINS


class Document(object):

    def __init__(self, id, text, status, comment, username):
        self.id = id
        self.text = text
        self.status = status
        self.comment = comment
        self.username = username

    def toJSON(self):
        return {
            'id': self.id,
            'text': self.text,
            'comment': self.comment,
            'status': self.status,
            'username': self.username}


class Database(object):

    def __init__(self):
        self.conn = sqlite3.connect(config.DATABASE_FILE)
        self.conn.isolation_level = None

    def getDocument(self, id):
        row = self.conn.execute('SELECT * FROM articles WHERE fileid = ?', (id,)).fetchone()
        return Document(*row) if row else None

    def setDocumentComment(self, username, id, comment):
        sql = """
            UPDATE articles SET comment = ?3
            WHERE fileid = ?2 AND username = ?1"""
        return bool(self.conn.execute(sql, (username, id, comment)).rowcount)

    def setDocumentStatus(self, username, id, status):
        sql = """
            UPDATE articles
            SET status = ?3, username = ?1
            WHERE fileid = ?2 AND ((status != "locked" AND ?3 = "locked") OR
                                 (status = "locked" AND username = ?1))"""
        return bool(self.conn.execute(sql, (username, id, status)).rowcount)

    def getDocuments(self):
        sql = 'SELECT * FROM articles ORDER BY title'
        return [Document(*row) for row in self.conn.execute(sql)]

    def canSendXML(self, username, id):
        row = self.conn.execute('SELECT status, username FROM articles WHERE fileid = ?', (id,)).fetchone()
        if row:
            return row[0] == 'locked' and row[1] == username
        else:
            return None

    def getCurrentDocuments(self, username):
        sql = 'SELECT * FROM articles WHERE (status = "complete" OR status = "locked") AND username = ? ORDER BY title'
        return [Document(*row) for row in self.conn.execute(sql, (username,))]

    def getAvailableDocuments(self, username):
        sql = 'SELECT * FROM articles WHERE status = "unlocked"'
        if isAdmin(username):
            sql += ' OR status = "error"'
        sql += ' ORDER BY title'
        return [Document(*row) for row in self.conn.execute(sql)]

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    print "This is a module, don't run it as a program"
