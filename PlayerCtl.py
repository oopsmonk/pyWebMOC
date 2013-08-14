#!/usr/bin/env python

import moc
import traceback

def reset():
    try:
        #shuffle
        moc.disable_shuffle()
        #repeat all
        moc.enable_repeat()
        #auto play next
        moc.enable_autonext()
    except:
        print traceback.format_exc()
        return -1
    return 0

#check moc status.
def check():
    try:
        #start server if not running 
        if moc.get_state() == -1:
            moc.start_server()
            print "moc server state :", moc.get_state()

    except moc.MocError as err:
        print "Error: ", err
        print "install mocp on Ubuntu : 'sudo apt-get install moc' "
        return -1
    return 0

#get current play list from moc.
def getFileList():
    plist = moc.get_playlist()
    flist = []
    for i in range(len(plist)):
        flist.append(plist[i][1])
    return flist

# 0:STOPPED 1:PAUSED 2:PLAYING -1: Server not running
def getStatus():
    try:
        st = moc.get_state()
        # fouce server start
        if st == -1:
            moc.start_server()

        st = moc.get_state()
    except:
        print traceback.format_exc()
        return -1
    print "moc state  = ", st
    return st

#moc info
def getInfo():
    try:
        if moc.get_state() == -1:
            moc.start_server()
        info = moc.get_info()
    except:
        print traceback.format_exc()
        return -1

    return info

#doPrev will change state to STOP if playing frist song.
def doPrev():
    if moc.is_playing() == True:
        moc.prev()
    else:
        return "moc server not running"

    return 0

def doPlay():
    print "doPlay..."
    try:
        st = getStatus() 

        if st == 0:
            plist = getFileList()
            print "Playlist : " , plist
            moc.play(plist)
        elif st == 1:
            moc.resume()

    except:
        print traceback.format_exc()
        return -1

    return 0

def doPause():
    try:
        st = getStatus() 
        if st == 2:
            moc.pause()
    except:
        print traceback.fomrmat_exc()
        return -1
    return 0

def doNext():
    try:
        moc.next()
    except:
        print traceback.fomrmat_exc()
        return -1
    return 0

def doStop():
    try:
        moc.stop()
    except:
        print traceback.fomrmat_exc()
        return -1
    return 0

def doQuit():
    try:
        moc.stop_server()
    except:
        print traceback.fomrmat_exc()
        return -1
    return 0


def doVolume(vol):
    return 0

def doSeek(sec):
    try:
        moc.seek(sec)
    except:
        print traceback.fomrmat_exc()
        return -1
    return 0
