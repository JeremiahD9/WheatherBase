/* Contributors: Noah */
// This code is to add suggestions to the search bar in map with countries that the user is typing into the search bar

$('#country-searchbar').on('keyup',function() {
    var user_input = $(this).val();
    $('#search-suggestions').empty(); //clears suggestions
    if(user_input.length>0){ 
        $.ajax({
            url: '/search-countries', //app.route function called in app.py
            type: 'GET',
            dataType: 'json',
            data: {'search': user_input},
            success: function(data){
                if(data){
                    var suggestionsList = $('<ul>');
                    $.each(data, function(index, country){
                        suggestionsList.append($('<li>').text(country));
                    });
                    $('#search-suggestions').append(suggestionsList);
                }
            },
            error: function(data){
                $('#search-suggestions').append('<p>No matching countries found.</p>');
            }
        });
    }
});