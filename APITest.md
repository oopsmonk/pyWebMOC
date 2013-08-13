#Test Server API use _curl_ tool  

##Player control  

ACTION: Prev, Play, Next, Stop, Pause, Quit  

    curl -X POST -H "Content-Type: application/json" -d '{"do":ACTION}' http://localhost:8080/pyWebMOC/ctl

ACTION: Volume  

    curl -X POST -H "Content-Type: application/json" -d '{"do":"Volume", "SetVolume":10}' http://localhost:8080/pyWebMOC/ctl  

ACTION: Seek

    curl -X POST -H "Content-Type: application/json" -d '{"do":"Seek", "doSeek":-20}' http://localhost:8080/pyWebMOC/ctl  


