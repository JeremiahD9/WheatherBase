// Get the current location
$.getJSON('https://ipinfo.io/geo', function(response) {
    var currentCountry = response.country;
    let regionNames = new Intl.DisplayNames(['en'], {type: 'region'});
    var currentCountryLong = regionNames.of(currentCountry);

    $.ajax({
        url: '/search-countries',
        type: 'GET',
        dataType: 'json',
        data: {'search': currentCountryLong},
        success: function(countryName) {
            document.getElementById("location").innerHTML = "Location: " + countryName;
            document.getElementById("secret-country").innerHTML = countryName;

            $.ajax({
                url: '/update-country',
                type: 'GET',
                dataType: 'json',
                data: {'country': document.getElementById("secret-country").innerText},
                success: function(countryData) {
                    var event = new Event('change');
                    document.getElementById("calendar").dispatchEvent(event);

                    lat = countryData['lat'];
                    lon = countryData['lon'];

                    // Initialize a new leaflet map
                    var map = new L.map('map').setView([lat, lon], 5);
                    window.map = map; //making it a global variable to be accessed in searchbar_scripts.js

                    // Create a new layer and add the map to the layer
                    var layer = new L.TileLayer("http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png");
                    map.addLayer(layer);

                    // Popup for current location
                    L.marker([lat, lon]).addTo(map);

                    //document.getElementById("location").innerHTML = "Location: " + country_long;
                }
            })
        }
    })
});

// Close the incorrect password error message
function closeError() {
    errorBox = document.getElementById("error-message");
    errorBox.style.display = "none";
}