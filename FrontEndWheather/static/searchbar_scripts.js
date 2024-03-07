/* Contributors: Noah */
// This code is to add suggestions to the search bar in map with countries that the user is typing into the search bar

variable = document.getElementById('#country-searchbar')

$('#country-searchbar').on('input',function() {
    var user_input = $(this).val();
    $('#search-suggestions').empty(); //clears suggestions
    if(user_input.length>0){ 
        $.ajax({
            url: '/search-countries', //app.route function called in app.py
            type: 'GET',
            dataType: 'json',
            data: {'search': user_input},
            success: function(country_names) {
                if(country_names){
                    var suggestionsContainer = $('<div>').addClass('search-suggestions');
                    $.each(country_names, function(index, country){
                        var button = $('<button>')
                            .addClass('suggestion-button')
                            .text(country)
                            .click(function() { //what to do after a country is clicked
                                $('#secret-country').text($(this).text());
                                $('#country-searchbar').val($(this).text());
                                $('#search-suggestions').empty(); // Clear suggestions
                                $('#location').empty();
                                updateMapLocation(country);
                            });
                        suggestionsContainer.append(button);
                    });
                    $('#search-suggestions').append(suggestionsContainer);
                }
            },
            error: function(data){
                $('#search-suggestions').append('<p>No matching countries found.</p>');
            }
        });
    }
});

function updateMapLocation(country){ 
    $('#location').text('Location: ' + country);
    $.getJSON('/update-country', {'country':country}, function(coords){ //goes to app.py
        console.log(coords);
        if(!coords.error){
            var newLat = coords.lat;
            var newLon = coords.lon;
            map.setView([newLat,newLon],5);

            L.marker([coords.lat, coords.lon]).addTo(map);

            var event = new Event('change');
            document.getElementById("calendar").dispatchEvent(event);
        }else{
            console.log("error2");
        }
    });
    
}