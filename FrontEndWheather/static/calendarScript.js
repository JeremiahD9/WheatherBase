// FILE CREATED BY NOAH

$('#calendar').on('change', function() {
    var selectedDate = $(this).val();
    var formattedDate = formatDate(selectedDate);
    var selectedCountry = $('#secret-country').text();
    $.getJSON('/get-map-data', {'country':selectedCountry, 'date':formattedDate}, function(data){ //goes to app.py
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

function formatDate(dateString) {
    var date = new Date(dateString);
    var day = date.getDate();
    var month = date.getMonth() + 1; // Months are zero indexed
    var year = date.getFullYear();

    return month + "/" + day + "/" + year;
}