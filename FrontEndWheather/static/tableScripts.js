// THIS FILE WILL BE EDITED BY JEREMIAH AND DAYA - LINKED TO TABLE.HTML

$('#calendar2').on('change',function() {
  var chosen_date = $(this).val();
  var chosen_country = $('#country-searchbar2').text();
  var isACountryChosen = false;
  if(chosen_country === ""){
    isACountryChosen = false;
  }else{
    isACountryChosen = true;
  }
  if(isACountryChosen==false){ 
    console.log(chosen_date,chosen_country,isACountryChosen)
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
            $("#myTable tr:not(.header)").remove();

            // Check if data is not empty
            if (Array.isArray(data) && data.length > 0) {
                
                $.each(data, function(index, row) {
                    console.log("Added row");
                    // Create a table row
                    var $tr = $('<tr>');
                    // Append table cells to the row
                    $tr.append($('<td>').text(row.country));
                    $tr.append($('<td>').text(row.location_name));
                    $tr.append($('<td>').text(row.lat));
                    $tr.append($('<td>').text(row.lon));
                    $tr.append($('<td>').text(row.timezone));
                    $tr.append($('<td>').text(row.last_updated));
                    $tr.append($('<td>').text(row.wind_mph));
                    $tr.append($('<td>').text(row.wind_degree));
                    $tr.append($('<td>').text(row.wind_direction));
                    $tr.append($('<td>').text(row.gust_mph));
                    $tr.append($('<td>').text(row.tempF));
                    $tr.append($('<td>').text(row.feels_like));
                    $tr.append($('<td>').text(row.pressure_in));
                    $tr.append($('<td>').text(row.precip_in));
                    $tr.append($('<td>').text(row.humidity));
                    $tr.append($('<td>').text(row.cloud));
                    $tr.append($('<td>').text(row.visibility_miles));
                    $tr.append($('<td>').text(row.uv_index));
                    $tr.append($('<td>').text(row.condition));
                    $tr.append($('<td>').text(row.co));
                    $tr.append($('<td>').text(row.ozone));
                    $tr.append($('<td>').text(row.no2));
                    $tr.append($('<td>').text(row.so2));
                    $tr.append($('<td>').text(row.pm25));
                    $tr.append($('<td>').text(row.pm10));
                    $tr.append($('<td>').text(row.epa));
                    $tr.append($('<td>').text(row.defra));
                    $tr.append($('<td>').text(row.sunrise));
                    $tr.append($('<td>').text(row.sunset));
                    $tr.append($('<td>').text(row.moonrise));
                    $tr.append($('<td>').text(row.moonset));
                    $tr.append($('<td>').text(row.moonphase));
                    $tr.append($('<td>').text(row.moon_illumination));
                    
                    // Append the row to the table
                    $('#myTable').append($tr);
                });
            } else {
                // If no data, append a message to that effect
                $('#myTable').append($('<tr>').append($('<td>').attr('colspan', '34').text('No data available for the selected date and country')));
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
