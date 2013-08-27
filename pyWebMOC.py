#!/usr/bin/env python

# Static Routes http://stackoverflow.com/questions/10486224/bottle-static-files

from bottle import route, static_file, debug, run, get, redirect
from bottle import post, request
import os, inspect, json
import PlayerCtl as player

#enable bottle debug
debug(True)

# WebApp route path
routePath = '/pyWebMOC'
# get directory of WebApp (pyWebMOC.py's dir)
rootPath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

@route(routePath)
def rootHome():
    #return redirect(routePath+'/index.html')
    return redirect(routePath+'/WebMOC.html')

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

* Play list
    * Append
    * add (clean old list)
    * clean

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
    #st = player.getStatus()
    #print "Get moc server status : %d" % st
    #return json.dumps({'Status':st})
    pinfo = player.getInfo()
    pinfo.update(player.getMiscInfo())
    print "Get info : \n", pinfo
    return json.dumps(pinfo)

#handle control post action
def CtlHandle(data):
    """
    request:
    {'do':action}
    response:
    {'ack': error}
    error:
    0: Success
    not zero: Failed.
    """
    if 'do' in data:
        #do action  parser
        ret = 0
        act = data.get('do')
        if act == 'Prev':
            ret = player.doPrev()
        elif act == 'Play':
            ret = player.doPlay()
        elif act == 'Next':
            ret = player.doNext()
        elif act == 'Stop':
            ret = player.doStop()
        elif act == 'Pause':
            ret = player.doPause()
        elif act == 'Volume':
            vol = data.get('SetVolume')
            ret = player.doVolume(int(vol))
        elif act == 'Quit':
            ret = player.doQuit()
        elif act == 'Seek':
            sec = data.get('doSeek')
            ret = player.doSeek(int(sec))
        elif act == 'Toggles':
            shuffle = data.get('Shuffle')
            repeat = data.get('Repeat')
            autoNext = data.get('AutoNext')
            if shuffle is not None:
                player.setShuffle(shuffle)
            if repeat is not None:
                player.setRepeat(repeat)
            if autoNext is not None:
                player.setAutoNext(autoNext)

        print "ret  = ", ret
        return json.dumps({'ack': ret})
    else:
        return json.dumps({'ack':-1})

#control POST API
@post(routePath + '/ctl')
def MOCControlPOST():
    data = request.json
    if data == None:
        return json.dumps({'ack': -1})

    print "Get cmd : ", data
    return CtlHandle(data)


#get playlist 
@get(routePath + '/playlist')
def MOCPlaylistGET():
    plist = player.getSongList()
    print "Get Playlist : \n", plist
    return json.dumps({"playlist":plist})

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


if player.check() == 0:
    player.resetPlayer()
    run(host='localhost', port=8080, reloader=True) #debug
#    run(host='localhost', port=8080)

