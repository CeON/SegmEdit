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


import os

SERVER_ROOT = os.path.realpath(os.path.dirname(__file__))

DEBUG = True

XMLS_DIR = SERVER_ROOT + os.path.sep + 'xmls'
PDFS_DIR = SERVER_ROOT + os.path.sep + 'pdfs'
DATABASE_FILE = SERVER_ROOT + os.path.sep + 'db.sqlite'

ADMINS = set(['admin'])

HOST = '0.0.0.0'
PORT = 7171

if __name__ == "__main__":
    print "This is a module, don't run it as a program"
