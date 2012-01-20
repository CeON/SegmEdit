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


from __future__ import with_statement

import os.path
import config
import json
from db import Database
from bottle import route, run, static_file, debug, response, install, \
    HTTPResponse, post, request, template, get

def as_json(callback):
    def default(obj):
        if hasattr(obj, 'toJSON'):
            return obj.toJSON()
        else:
            raise TypeError
    def wrapper(*args, **kwargs):
        result = callback(*args, **kwargs)
        if isinstance(result, HTTPResponse):
            return result
        else:
            response.content_type = 'application/json'
            return json.dumps(result, default=default)
    return wrapper

def use_db(callback):
    def wrapper(*args, **kwargs):
        db = Database()
        try:
            result = callback(db=db, *args, **kwargs)
        finally:
            db.close()
        return result
    return wrapper

install(as_json)
install(use_db)


@route('/:username/xmls/:id')
def xmls(username, id, db):
    doc = db.getDocument(id)
    return static_file('%s.xml' % doc.id, root=config.XMLS_DIR)


@route('/:username/pdfs/:id')
def pdfs(username, id, db):
    doc = db.getDocument(id)
    return static_file('%s.pdf' % doc.id, root=config.PDFS_DIR)


@route('/:username/documents/:id')
def documents(username, id, db):
    return db.getDocument(id)


@route('/:username/list_current')
def listCurrent(username, db):
    return db.getCurrentDocuments(username)


@route('/:username/list_available')
def listAvailable(username, db):
    return db.getAvailableDocuments(username)


@post('/:username/send/:id')
def send(username, id, db):
    data = request.files.get('file')
    if config.DEBUG:
        print 'data is not None?', bool(data is not None)
        if data is not None:
            print 'data.file?', bool(data.file)
        print 'canSendXML?', db.canSendXML(username, id)
    if data is not None and data.file and db.canSendXML(username, id):
        blocksize = 8192
        with open(config.XMLS_DIR + os.path.sep + '%s.xml' % id, 'w') as f:
            block = data.file.read(blocksize)
            while block:
                f.write(block)
                block = data.file.read(blocksize)
        return True
    else:
        return False


@get('/:username/set_status/:id')
def setStatus(username, id, db):
    status = request.GET.get('status', '')
    if status not in ['unlocked', 'locked', 'complete', 'error']:
        if config.DEBUG:
            print 'Invalid status: %s' % status
        return False
    else:
        return db.setDocumentStatus(username, id, status)


@get('/:username/set_comment/:id')
def setComment(username, id, db):
    comment = request.GET.get('comment', '').decode('utf-8')
    return db.setDocumentComment(username, id, comment)


@route('/', skip=[as_json])
def index(db):
    docs = db.getDocuments()
    counts = dict(unlocked=0, locked=0, error=0, complete=0)
    for doc in docs:
        counts[doc.status] += 1
    return template('summary', documents=docs, **counts)


if __name__ == "__main__":
    if config.DEBUG:
        debug(True)
        run(host=config.HOST, port=config.PORT, reloader=True)
    else:
        run(host=config.HOST, port=config.PORT)
