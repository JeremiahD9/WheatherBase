// FILE CREATED BY NOAH

$('#calendar').on('change', function() {
    var selectedDate = $(this).val();
    var selectedCountry = $('#secret-country').val();
    $.getJSON('/get-map-data', {'country':selectedCountry, 'date':selectedDate}, function(data){ //goes to app.py
        console.log(data);
        if(!data.error){
            var temp = data.temp;
            var wind = data.wind;
            var precip = data.precip;
            var sunrise = data.sunrise;
            var sunset = data.sunset;
            var moonphase = data.moonphase;
        }else{
            console.log("error2");
        }
    });
});