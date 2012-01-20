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


from db import Database
import sys
from getopt import getopt


def main():
    opts, args = getopt(sys.argv[1:], '', ('prefix=', 'suffix=', 'status=', 'user='))
    opts = dict(opts)
    prefix = opts.get('--prefix', '')
    suffix = opts.get('--suffix', '')
    status = opts.get('--status')
    username = opts.get('--user')

    db = Database()
    for doc in db.getDocuments():
        if status is not None and doc.status != status:
            continue
        if username is not None and doc.username != username:
            continue
        print prefix + doc.id + suffix


if __name__ == "__main__":
    main()
