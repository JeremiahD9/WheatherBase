// FILE CREATED BY NOAH

$('#calendar').on('change', function() {
    var selectedDate = $(this).val();
    var selectedCountry = $('#secret-country').text();

    $.ajax({
        url: '/get-map-data',
        type: 'GET',
        dataType: 'json',
        data: {
            'country': selectedCountry,
            'date': selectedDate
        },
        success: function(weatherValues) {
            console.log(data);
            $('#temp-val').text(weatherValues[0] + ' °C');
            $('#wind-val').text(weatherValues[1] + ' km/h');
            $('#precip-val').text(weatherValues[2] + ' mm');
            $('#sunrise-val').text(weatherValues[3]);
            $('#sunset-val').text(weatherValues[4]);
            $('#moon-val').text(weatherValues[5]);
        }
    });
});