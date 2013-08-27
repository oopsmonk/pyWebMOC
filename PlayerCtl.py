#!/usr/bin/env python

#http://moc.lophus.org/
import moc
import math
import traceback

gCurrVolume = 10 

gIsShuffle = False
gIsRepeat = True
gIsAutoNext = True

def setShuffle(isOn):
    global gIsShuffle
    if type(isOn) is bool:
        gIsShuffle = isOn 
    else:
        if isOn in ['On', 'on']:
            gIsShuffle = True
        else:
            gIsShuffle = False

    print "set Shuffle : ", gIsShuffle 
    if gIsShuffle:
        moc.enable_shuffle()
    else:
        moc.disable_shuffle()

def isShuffle():
    global gIsShuffle
    return gIsShuffle

def setRepeat(isOn):
    global gIsRepeat
    if type(isOn) is bool:
        gIsRepeat = isOn 
    else:
        if isOn in ['On', 'on']:
            gIsRepeat = True
        else:
            gIsRepeat = False
    
    if gIsRepeat:
        moc.enable_repeat()
    else:
        moc.disable_repeat()

def isRepeat():
    global gIsRepeat
    return gIsRepeat

def setAutoNext(isOn):
    global gIsAutoNext
    if type(isOn) is bool:
        gIsAutoNext = isOn 
    else:
        if isOn in ['On', 'on']:
            gIsAutoNext = True
        else:
            gIsAutoNext = False
    
    if gIsAutoNext:
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

    info_dict = getInfo()
    gCurrVolume = int(info_dict.get('volume'))
    print("get volume", gCurrVolume)
    return gCurrVolume

def VolumeUp(num):
    global gCurrVolume
    gCurrVolume += num
    moc.volume_up(num)

def VolumeDown(num):
    global gCurrVolume
    gCurrVolume -= num
    moc.volume_down(num)

def resetPlayer():
    print "Player reset"
    #shuffle
    setShuffle(False)
    #repeat all
    setRepeat(True)
    #auto play next
    setAutoNext(True)
    # set defualt volume
    getVolume()

#check moc status.
def check():
    try:
        #start server if not running 
        if moc.get_state() == -1:
            moc.start_server()
            print "moc server state :", moc.get_state()

        #get defutal status

    except moc.MocError as err:
        print "Error: ", err
        print "install mocp on Ubuntu : 'sudo apt-get install moc' "
        return -1
    return 0

#get current song list from moc.
def getSongList():
    plist = moc.get_playlist()
    flist = []
    for i in range(len(plist)):
        flist.append(plist[i][0])
    return flist

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

#boolean value to On/Off string
def toOnOff(b):
    if b:
        return "On"
    return "Off"

#get Volume, Shuffle, Repeat, AutoNext info.
def getMiscInfo():
    global gIsShuffle, gIsRepeat, gIsAutoNext
    
    return {'Shuffle': toOnOff(gIsShuffle),
            'Repeat': toOnOff(gIsRepeat),
            'AutoNext': toOnOff(gIsAutoNext)}

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
            #moc.play(plist)
            moc.quickplay(plist)
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

def doPlayNum(index):
    try:
        moc.play_num(int(index))
    except:
        print traceback.fomrmat_exc()
        return -1
    return 0

