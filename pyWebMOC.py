#!/usr/bin/env python

# Static Routes http://stackoverflow.com/questions/10486224/bottle-static-files

from bottle import route, static_file, debug, run, get, view, redirect
from bottle import post
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

#http://gotofritz.net/blog/weekly-challenge/restful-python-api-bottle/
@get(routePath + '/jsontest')
def returnJSON():
    return {"id":1,"name":"Sam"}

@post(routePath + '/postTest')
def testPost():
    return {"id":2,"name":"OopsMonk"}

@get(routePath + '/gettest')
def gettest():
    return "get test return!!!\n"

run(host='localhost', port=8080, reloader=True)

