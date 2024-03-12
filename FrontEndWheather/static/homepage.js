// Get the current location
$.getJSON('https://ipinfo.io/geo', function(response) {
    var coords = response.loc.split(",");
    $.ajax({
        url: "https://wttr.in/" + Math.round(coords[0]*100)/100 + "," + Math.round(coords[1]*100)/100 + "?T",
        success: function(data) {
            console.log(data);

            document.getElementById("current-weather").innerHTML = data;
        }
    })
});