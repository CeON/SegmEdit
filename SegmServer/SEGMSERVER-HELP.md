# SegmServer

## Introduction

SegmServer is a part of SegmEdit, a tool for viewing and correcting server XML
files in TrueViz format. SegmServer is useful for managing a network repository
of documents processed with SegmEditGUI application. The server is able to
distribute documents to multiple SegmEditGUI instances, receiving partly or
completely processed files and gathering and presenting the results of file
processing.

SegmServer requires `Python` (it has been tested using `Python 2.6` and `2.7`)
and `Bottle Python Web Framework`.

## Running the server

### Preparing files

For every document to be managed by the server a pair of files should be
prepared: PDF and XML TrueViz. The files should have the same name with
extensions: `.pdf` and `.xml` respectively (lower case). All PDF and XML files
have to be placed in directories `pdfs` and `xmls`, respectively (directories
paths are configurable).

### Preparing the database

All the files to be managed by SegmServer have to be indexed in the database. To
perform this step, type:

    ./manage_articles.py sync_db

There are other options, that can be passed to `manage_articles.py`, including
options responsible for database reset, adding a single document, removing a
document, listing available documents). To check all available options, type:

    ./manage_articles help

### HTTP server

The simplest way to run the server is to open the screen session and type:

    ./server.py 2>&1 >> server.log

SegmServer listens on configured port (default is 7171) on all network
interfaces. `server.log` file receives all log messages from the server.

## Server status

SegmServer stores statistics about managed documents. Such information,
including document identifier, title, status, user and comment (more information
in the [SegmEditGUI
help](https://github.com/CeON/SegmEdit/blob/master/SegmEditGUI/SEGMEDITGUI-HELP.md))
can be accessed at `http://server:port/`.

## Configuration

SegmServer stores its configuration in `config.py` file. If anything is modified
there, Python syntax should be preserved. Configuration file contains numerous
options, including: 

* HOST - IP address, on which the server listen for incoming requests. Default
value is 0.0.0.0, which means listening on all interfaces.
* PORT - port number, default value is 7171.
* XMLS_DIR - path to directory storing XML files.
* PDFS_DIR - path directory storing PDF files.
* ADMINS - list of privileges users (they can access all documents, including
those locked by other users)

## Security

SegmServer does not include have any security mechanism. The best way to use it
is to run it in isolated and secured network. The server allows for simple user
identification, but without any authentication mechanisms. If there is a need to
increase the security level, the files should be managed and distributed in
other way.
