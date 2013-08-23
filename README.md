#pyWebMOC  
This is a web service for control MOC on Linux and Raspberry pi.  

##Requires  
moc  
python-bottle  
python-moc  

##Features  

* Control MOC player from web GUI.  
    Play, Pause, Next, Previous, Stop, Seek, Volume, Shuffle, Repeat, AutoNext  
    __(Currently, Volume control failed on Raspberry pi)__  

* Cannot change playing song via playlist, because MOC not provide this kinds of APIs.  

* Display infos.
    playlist, song title, artist, duration.  
    TODO: bitrate, rate.

