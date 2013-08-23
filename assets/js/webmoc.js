/*
 * Control MOC player on Server. 
 *
 *
 */
$(document).ready(function(){
//    alert("Doc ready");
});
$(document).bind('pageinit', function(){
    //alert("page init done!");

    //convert String to HHMMSS
    String.prototype.toHHMMSS = function () {
        var sec_num = parseInt(this, 10); 
        var hours   = Math.floor(sec_num / 3600);
        var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
        var seconds = sec_num - (hours * 3600) - (minutes * 60);

        if (hours   < 10) {hours   = "0"+hours;}
        if (minutes < 10) {minutes = "0"+minutes;}
        if (seconds < 10) {seconds = "0"+seconds;}
        var time = 0;
        if( parseInt(hours) == 0 )
           time = minutes+':'+seconds;
        else
            time = hours+':'+minutes+':'+seconds;        
        return time;
    }

    //convert time HH:mm:ss to seconds
    function HHMMtoSec(t){
        var array_t = t.split(":");
        var seconds = 0;
        if (array_t.length == 2) {
            seconds = (+array_t[0]) * 60 + (+array_t[1]);
        } else if (array_t.length == 3) {
            seconds = (+array_t[0]) * 60 * 60 + (+array_t[1]) * 60 + (+array_t[2]);
        }
        return seconds;
    }

    //get moc server info
    function getInfo(){
    
        $.getJSON(ctlpage, function(data){
            $.each(data, function(index, value){
                //alert("index: " + index + " , value: "+ value);
                if(index == "state"){
                    gPlayerState = value;
                }

                if(index == "artist"){
                    gArtist = value;
                    $('#song-artist').html(gArtist);
                }

                if(index == "songtitle"){
                    gSongTitle = value;
                    $('#song-title').html(gSongTitle);
                }

                if(index == "Shuffle"){
                    if(gShuffle != value){
                        //alert(index + " = " + value);
                        gShuffle = value;
                        $('#swShuffle').val(gShuffle).slider('refresh');
                    }       
                }

                if(index == "Repeat"){
                    if(gRepeat != value){
                        gRepeat = value;
                        $('#swRepeat').val(gRepeat).slider('refresh');
                        //alert(index + " = " + value);
                    }
                }

                if(index == "AutoNext"){
                    if(gAutoNext != value){
                        gAutoNext = value;
                        $('#swAutoNext').val(gAutoNext).slider('refresh');
                        //alert(index + " = " + value);
                    }
                }
                
                if(index =="Volume"){
                    if(gVolume != value){
                        gVolume = value;
                        //alert(index + " = " + value);
                        $('#slider-vol').val(gVolume).slider('refresh');
                    }
                }

                if(index == "totaltime"){
                    if(gTotalTime != value){
                        gTotalTimeMMSS = value;
                        gTotalTime = HHMMtoSec(value);
                        $('#slider-time').attr("max", gTotalTime);
                    }
                }

                if(index == "currentsec"){
                    if(gCurrTime != value){
                        if($('#slider-time').is(":disabled")){
                            $('#slider-time').slider('enable');
                        }
                        gCurrTime = value;
                        $('#slider-time').val(gCurrTime).slider('refresh');
                    }
                }


            });
        });    
    }

    //post json
    function actionEmit(jdata){
        $.ajax({
            type: 'POST',
            url: ctlpage,
            data:JSON.stringify(jdata),
            contentType: "application/json; charset=utf-8",
            dataType: 'json',
            success: function(data){
                $.each(data, function(index, value){
                    //alert("index: " + index + " , value: "+ value);
                    if(index == "ack" && value != 0)
                        alert("Error : " + value);
                });
            }
        });
        
    }


    var ctlpage = 'ctl';
    var gShuffle = 'Off';
    var gRepeat = 'Off';
    var gAutoNext = 'Off';
    var gVolume = 0;
    var gTotalTime = 0;
    var gTotalTimeMMSS = "00:00";
    var gCurrTime = 0;
    var gPlayerState = 0;
    var gSongTitle ="";
    var gArtist = "";
    var gInfoDelay = 1000;
    var gUpdateTime = 1000;

    //http://code.google.com/p/jquery-timer/
    var infoTrigger = $.timer(function(){
        
        if(gPlayerState == 2){
            if((gCurrTime >= gTotalTime) || (gCurrTime == 0)){
                getInfo();

            }else{
                gCurrTime = parseInt(gCurrTime) + 1;
                if($('#slider-time').is(":disabled")){
                    $('#slider-time').slider('enable');
                }
                $('#slider-time').val(gCurrTime).slider('refresh');
            }
        }
        
    });


    //button action 
    $('#btnPrev').click(function(){
        actionEmit({"do":"Prev"});
        if(!infoTrigger.isActive)
            infoTrigger.play();  
        setTimeout(function(){getInfo();},gInfoDelay);
    });

    $('#btnPlay').click(function(){
        actionEmit({"do":"Play"});
        infoTrigger.play();        
        setTimeout(function(){getInfo();},gInfoDelay);
    });

    $('#btnNext').click(function(){
        actionEmit({"do":"Next"});
        if(!infoTrigger.isActive)
            infoTrigger.play();  
        setTimeout(function(){getInfo();},gInfoDelay);
    });
    
    $('#btnPause').click(function(){
        actionEmit({"do":"Pause"});
        if(infoTrigger.isActive)
            infoTrigger.stop();  
        else
            infoTrigger.play();
        setTimeout(function(){getInfo();},gInfoDelay);
    });

    $('#btnStop').click(function(){
        actionEmit({"do":"Stop"});
        infoTrigger.stop();        
    });

    //Toggle switch
    $('#swShuffle').change(function(){
        //set value to player
        //alert("Toggle Shuffle set : " + $(this).val());
        var value = $(this).val();
        if (value != gShuffle){
            gShuffle = value
            actionEmit({"do":"Toggles", "Shuffle":value});
        }
    });

    $('#swRepeat').change(function(){
        //set value to player
        var value = $(this).val();
        if (value != gRepeat){
            gRepeat = value
            actionEmit({"do":"Toggles", "Repeat":value});
        }
    });

    $('#swAutoNext').change(function(){
        //set value to player
        var value = $(this).val();
        if (value != gAutoNext){
            gAutoNext = value
            actionEmit({"do":"Toggles", "AutoNext":value});
        }
    });

    //Volume slider
    $('#slider-vol').on('slidestop', function(event){
        actionEmit({"do":"Volume", "SetVolume":$(this).val()});
    });

    //time bar
    if(gCurrTime == 0){
        $('#slider-time').slider('disable');
    }
    $('#slider-time').attr({
        "min": 0, 
        "max": gTotalTime,
        "step": 1});

    $('#slider-time').val(gCurrTime).slider('refresh');

    $('#slider-time').on('slidestart', function(event, ui){
        infoTrigger.stop();        
    });
    $('#slider-time').on('slidestop', function(event, ui){
        var v = $(this).val() - gCurrTime;

        //alert("do seek to " + v );
        actionEmit({"do":"Seek", "doSeek": v});
        getInfo();
        infoTrigger.play();
    });
    
    //Get init data from server
    getInfo();

    //start info timer
    infoTrigger.set({time:1000, autostart:true});

}); //End of Page init


