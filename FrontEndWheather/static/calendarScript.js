// FILE CREATED BY NOAH

$('#calendar').on('change', function() {
    var selectedDate = $(this).val();
    var selectedCountry = $('#secret-country').text();
    $.getJSON('/get-map-data', {'country':selectedCountry, 'date':selectedDate}, function(data){ //goes to app.py
        console.log(data);
        if(!data.error){
            $('#temp-val').text(data.temp + ' °C');
            $('#wind-val').text(data.wind + ' km/h');
            $('#precip-val').text(data.precip + ' mm');
            $('#sunrise-val').text(data.sunrise);
            $('#sunset-val').text(data.sunset);
            $('#moon-val').text(data.moonphase);
        }else{
            console.log("error2");
        }
    });
});