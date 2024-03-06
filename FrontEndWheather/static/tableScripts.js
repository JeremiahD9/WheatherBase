// THIS FILE WILL BE EDITED BY JEREMIAH AND DAYA - LINKED TO TABLE.HTML

function initializeTable(){
    $.getJSON('/init-table', {'country':None}, function(rows){ //goes to app.py - ADD MORE ROWS YOU WANT TO ADD
        console.log("PYTHON CODE RAN");
        if(!rows.error){
            var newLat = coords.lat;
            var newLon = coords.lon;
            map.setView([newLat,newLon],5);
        }else{
            console.log("error2");
        }
    });
}

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
