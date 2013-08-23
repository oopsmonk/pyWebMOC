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

##Server API test use curl  

ACTION: Prev, Play, Next, Stop, Pause, Quit  

    curl -X POST -H "Content-Type: application/json" -d '{"do":ACTION}' http://localhost:8080/pyWebMOC/ctl

Example of Play action:  

    curl -X POST -H "Content-Type: application/json" -d '{"do":"Play"}' http://localhost:8080/pyWebMOC/ctl  


Example of Volume set to 10:  

    curl -X POST -H "Content-Type: application/json" -d '{"do":"Volume", "SetVolume":10}' http://localhost:8080/pyWebMOC/ctl

Example of Seek -20:  

    curl -X POST -H "Content-Type: application/json" -d '{"do":"Seek", "doSeek":-20}' http://localhost:8080/pyWebMOC/ctl

Example of get info:  

    curl -X GET http://localhost:8080/pyWebMOC/ctl  

Example of get Playlist:  

    curl -X GET http://localhost:8080/pyWebMOC/playlist

