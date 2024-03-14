# WheatherBase

This is a weather repository created by Noah Lee, Warren Kozak, Daya Tucker and Jeremiah Dawson as the final project for CS 257 Software Design taught by Matt Lepinski (March 7th 2024).

In order to run this program, on a stearns server, run the file app.py in the terminal. To view the website, go to a browser and paste the following url: http://stearns.mathcs.carleton.edu:5127/

This project was done using a Flask python API, PSQL, HTML, CSS and JavaScript. The data used for this project was downloaded from kaggle - https://www.kaggle.com/datasets/nelgiriyewithana/global-weather-repository and the map used in map.html uses google maps existing technology. 

This website allows users to register to create an account to login.  Upon login, the site directs the user to the homepage which displays the current weather as well as the forecast for the next two days.

The 'Map' section prompts the user to enter the name of a country as well as a specific date, and displays the selected country on the map, with the weather information for the selected date listed on the left side of the screen.

The 'Table' section displays a table containing the weather data for every country on the date specified by the user.  

In the 'Horoscope' section, users are able to view past weather data on map and table form, as well as calculate an arbitrary 'horoscope' value, using weather data calculated with their birthday and birthplace.
