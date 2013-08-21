#!/usr/bin/env python

#http://moc.lophus.org/
import moc
import math
import traceback


gInitVolume = 20
gCurrVolume = gInitVolume

gIsShuffle = "Off"
gIsRepeat = "On"
gIsAutoNext = "On"

tupleTrue = ['True','ture',1,'On','on']

def setShuffle(isOn):
    global gIsShuffle
    gIsShuffle = isOn 
    print "set Shuffle : ", gIsShuffle 
    if isOn in ["on","On"]:
        moc.enable_shuffle()
    else:
        moc.disable_shuffle()

def isShuffle():
    global gIsShuffle
    return gIsShuffle

def setRepeat(isOn):
    global gIsRepeat
    gIsRepeat = isOn 
    if isOn in ["on","On"]:
        moc.enable_repeat()
    else:
        moc.disable_repeat()

def isRepeat():
    global gIsRepeat
    return gIsRepeat

def setAutoNext(isOn):
    global gIsAutoNext
    gIsAutoNext = isOn 
    if isOn in ["on","On"]:
        moc.enable_autonext()
    else:
        moc.disable_autonext()

def isAutoNext():
    global gIsAutoNext
    return gIsAutoNext

def setVolume(v):
    global gCurrVolume
    tmp = v - gCurrVolume
    if tmp < 0 :
        moc.volume_down(math.fabs(tmp))
        gCurrVolume += tmp
    elif tmp > 0 :
        moc.volume_up(tmp)
        gCurrVolume += tmp
    print "Volume set to " , gCurrVolume

def getVolume():
    global gCurrVolume
    return gCurrVolume

def resetVolume():
    global gCurrVolume, gInitVolume
    moc.volume_down(100)
    moc.volume_up(gInitVolume)
    gCurrVolume = gInitVolume
    print "Reset volume: " , gCurrVolume


def VolumeUp(num):
    global gCurrVolume
    gCurrVolume += num
    moc.volume_up(num)

def VolumeDown(num):
    global gCurrVolume
    gCurrVolume -= num
    moc.volume_down(num)

def resetPlayer():
    #shuffle
    setShuffle(False)
    #repeat all
    setRepeat(True)
    #auto play next
    setAutoNext(True)
    # set defualt volume
    resetVolume()
    print "Player reset"

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

#get Volume, Shuffle, Repeat, AutoNext info.
def getMiscInfo():
    global gCurrVolume, gIsShuffle, gIsRepeat, gIsAutoNext
    
    return {'Volume': gCurrVolume,
            'Shuffle': gIsShuffle,
            'Repeat': gIsRepeat,
            'AutoNext': gIsAutoNext}

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
        moc.toggle_pause()
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
    setVolume(vol)
    return 0 

def doSeek(sec):
    try:
        moc.seek(sec)
    except:
        print traceback.fomrmat_exc()
        return -1
    return 0


