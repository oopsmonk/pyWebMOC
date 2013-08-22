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

    //get moc server info
    function getInfo(){
    
        $.getJSON(ctlpage, function(data){
            $.each(data, function(index, value){
                //alert("index: " + index + " , value: "+ value);
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


    var ctlpage = 'ctl';
    var gShuffle = 'Off';
    var gRepeat = 'Off';
    var gAutoNext = 'Off';
    var gVolume = 0;
    var gTotalTime = 0;
    var gCurrTime = 0;
    var gPlayerState = 0;

    //http://code.google.com/p/jquery-timer/
    var infoTrigger = $.timer(function(){
        //alert("getInfo");
        getInfo();
    });
    infoTrigger.set({time:1000, autostart:true});

    //Get init data from server
    getInfo();


    //button action 
    $('#btnPrev').click(function(){
        actionEmit({"do":"Prev"});
    });

    $('#btnPlay').click(function(){
        actionEmit({"do":"Play"});
        infoTrigger.play();        
    });

    $('#btnNext').click(function(){
        actionEmit({"do":"Next"});
    });
    
    $('#btnPause').click(function(){
        actionEmit({"do":"Pause"});
        if(infoTrigger.isActive)
            infoTrigger.stop();  
        else
            infoTrigger.play();
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
        infoTrigger.play();
    });
    
}); //End of Page init


