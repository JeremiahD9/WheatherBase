// THIS FILE WILL BE EDITED BY JEREMIAH AND DAYA - LINKED TO TABLE.HTML

$('#calendar2').on('change',function() {
  var chosen_date = $(this).val();
  var chosen_country = $('#country-searchbar2').text();
  var isACountryChosen = false;
  if(chosen_country.equals("Put a new country...")){
    isACountryChosen = false;
  }else{
    isACountryChosen = true;
  }
  if(user_input.length>0){ 
      $.ajax({
          url: '/use-date-to-get-data', //app.route function called in app.py
          type: 'GET',
          dataType: 'json',
          data: {
            'date': chosen_date,
            'country': chosen_country,
            'isACountryChosen': isACountryChosen
          },
          success: function(data) {
              if(data){
                  var suggestionsContainer = $('<div>').addClass('search-suggestions');
                  $.each(country_names, function(index, country){
                      var button = $('<button>')
                          .addClass('suggestion-button')
                          .text(country)
                          .click(function() { //what to do after a country is clicked
                              $('#country-searchbar2').val($(this).text());
                              $('#search-suggestions2').empty(); // Clear suggestions
                          });
                      suggestionsContainer.append(button);
                  });
                  $('#search-suggestions2').append(suggestionsContainer);
              }
          },
          error: function(data){
              $('#search-suggestions2').append('<p>No matching countries found.</p>');
          }
      });
  }
});

function myFunction() {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
    
}
