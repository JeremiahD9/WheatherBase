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
        success: function(data) {
            $('#temp-val').text(data[0] + ' °C');
            $('#wind-val').text(data[1] + ' km/h');
            $('#precip-val').text(data[2] + ' mm');
            $('#sunrise-val').text(data[3]);
            $('#sunset-val').text(data[4]);
            $('#moon-val').text(data[5]);
        }
    });
});