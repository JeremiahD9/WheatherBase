// Contributors: Noah, Warren

$('#calendar').on('change', function() {
    console.log("function ran 1");
    var inputDate = $(this).val();
    var selectedCountry = $('#secret-country').text();
    var selectedDate = convertDateFormat(inputDate);

    $.ajax({
        url: '/get-map-data',
        type: 'GET',
        dataType: 'json',
        data: {
            'country': selectedCountry,
            'date': selectedDate
        },
        success: function(data) {
            console.log("function ran 1");
            $('#temp-val').text(data[0] + ' °C');
            $('#wind-val').text(data[1] + ' km/h');
            $('#precip-val').text(data[2] + ' mm');
            $('#sunrise-val').text(data[3]);
            $('#sunset-val').text(data[4]);
            $('#moon-val').text(data[5]);
        }
    });
});

function convertDateFormat(dateStr) {
    var dateObj = new Date(dateStr);

    var month = dateObj.getUTCMonth() + 1;
    var day = dateObj.getUTCDate();
    var year = dateObj.getUTCFullYear();

    var newDateStr = month + "/" + (day < 10 ? "0" + day : day) + "/" + year;

    return newDateStr;
}