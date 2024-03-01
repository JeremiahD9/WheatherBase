// THIS FILE WILL BE EDITED BY JEREMIAH AND DAYA - LINKED TO TABLE.HTML

function initializeTable(){
    $.getJSON('/init-table', {'country':country, 'temp': tempc}, function(rows){ //goes to app.py - ADD MORE ROWS YOU WANT TO ADD
        console.log("PYTHON CODE RAN");
        if(!rows.error){
            var newLat = coords.lat;
            var newLon = coords.lon;
            map.setView([newLat,newLon],5);
        }else{
            console.log("error2");
        }
    });
}