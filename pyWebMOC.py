#!/usr/bin/env python

from bottle import route, static_file, error, debug, run, get, view, redirect

debug(True)

routePath = '/pyWebMOC'
rootPath = './'

@route(routePath)
def rootHome():
    return redirect(routePath+'/index.html')

@view(routePath + '/index.html')
def home():
    return static_file("index.html", root=rootPath)

@get(routePath + '/images/:filename')
def fonts(filename):
    return static_file(filename, root=rootPath+'assets/js/images')

# Static Routes http://stackoverflow.com/questions/10486224/bottle-static-files
#@get(routePath + '/<filename:re:.*\.js>')
@route(routePath + '/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root=rootPath+'assets/js')

#@get(routePath + '/<filename:re:.*\.css>')
@route(routePath + '/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root=rootPath+'assets/css')

@get(routePath + '/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root=rootPath+'assets/img')

#@get(routePath + '/<filename:re:.*\.html>')
@route(routePath + '/<filename:re:.*\.html>')
def html(filename):
    return static_file(filename, root=rootPath)

run(host='localhost', port=8080, reloader=True)
