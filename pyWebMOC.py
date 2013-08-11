#!/usr/bin/env python

# Static Routes http://stackoverflow.com/questions/10486224/bottle-static-files

from bottle import route, static_file, debug, run, get, view, redirect
from bottle import post, request, response
import os, inspect, json
import moc

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

"""
Function list
* Player control GET
    * return moc server state (play/stop/pause/not running)

* Player control POST
    * Previous
    * Play / Resume
    * Next
    * Pause
    * Stop
    * volume

* Player info
    * Song name
    * current time
    * duration
    * 
"""

#control GET API return 
@get(routePath + '/ctl')
def MOCControlGET():
    """
    -1: moc server not running 
    0: Stopping
    1: Pause
    2: Playing
    """
    st = moc.get_state()
    print "Get moc server status : %d" % st
    return json.dumps({'Status':st})

#handle control post action
def CtlHandle(data):
    """
    request:
    {'do':action}
    action:
    0: Prev 
    1: Play/Pause
    2: Next
    3: Stop
    4: Volume
    5: Add playlist
    6: append playlist
    7: clear playlist
    8:
    response:
    {'ack': error}
    error:
    0: Success
    not zero: Failed.
    """

    return json.dumps({'ack':0})

#control POST API
@post(routePath + '/ctl')
def MOCControlPOST():
    data = request.json
    if data == None:
        return json.dumps({'ack': -1})

    print "Get cmd : %s" % data 
    return CtlHandle(data)

#http://gotofritz.net/blog/weekly-challenge/restful-python-api-bottle/
"""
POST action
curl -i -X GET http://localhost:8080/pyWebMOC/jsonGET

GET action
curl -X POST -H "Content-Type: application/json" -d '{"id":"1","name":"OopsMonk"}' http://localhost:8080/pyWebMOC/jsonPOST
"""
@get(routePath + '/json')
def testJsonGET():
    print dict(request.headers)
    return {"id":1,"name":"Sam"}

@post(routePath + '/json')
def testJsonPost():
    #print dict(request.headers)
    data = request.json
    print data
    if data == None:
        return json.dumps({'Status':"Failed!"})
    else:
        return json.dumps({'Status':"Success!"})

@get(routePath + '/gettest')
def gettest():
    return "get test return!!!\n"

run(host='localhost', port=8080, reloader=True)

