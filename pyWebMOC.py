#!/usr/bin/env python

# Static Routes http://stackoverflow.com/questions/10486224/bottle-static-files

from bottle import route, static_file, debug, run, get, view, redirect
import os, inspect

#enable bottle debug
debug(True)

# WebApp route path
routePath = '/pyWebMOC'
# get directory of WebApp (pyWebMOC.py's dir)
rootPath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

@route(routePath)
def rootHome():
    return redirect(routePath+'/index.html')

@view(routePath + '/index.html')
def home():
    return static_file("index.html", root=rootPath)

@route(routePath + '/<filename:re:.*\.html>')
def html_file(filename):
    return static_file(filename, root=rootPath)

@get(routePath + '/assets/<filepath:path>')
def assets_file(filepath):
    return static_file(filepath, root=rootPath+'/assets')

run(host='localhost', port=8080, reloader=True)

