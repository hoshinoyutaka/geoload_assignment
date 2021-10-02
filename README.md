#  Putting places on Google Map

A place could be anything - a restaurant, showplace or university name.

The task is to somehow collect the geographical data about the certain places and to use that data to put them on a Google Map.

To accomplisg that we divide the problem into several steps:
1. Collect the data about specified places(see where.data) using Geocoding API from Google. We want to make it an easy restartable process - simply request JSON from an API and then store that geocoded response in a database (geodata.sqlite). Before we use the geocoding API, we just check to see if we already have the data for that particular line of input. That's what the geoload.py does.
Here is a sample run after there is already some data in the database:
```
AGH University of Science and Technology is already in a database
Academy of Fine Arts Warsaw Poland is already in a database
American University in Cairo is already in a database
...
1) Retrieving University College Dublin...
2) Retrieving University Munich...
3) Retrieving University of Akron...
```
2. Once we have some data loaded into geodata.sqlite, we want to visualize the data using the (geodump.py) program. This program reads the database, parses JSON's and writes tile file (where.js) with the location, latitude, and longitude in the form of executable JavaScript code. 
A run of the geodump.py program is as follows:
```
...
10) 31.5488923; -97.1130573; 1311 S 5th St, Waco, TX 76706, USA
11) 39.9619537; 116.3662615; 19 Xinjiekou Outer St, Bei Tai Ping Zhuang, Beijing Shi, China, 100875
12) 53.8938988; 27.5460609; prasp. Niezaliežnasci 4, Minsk, Belarus
...
300 records were written in a my_where.js file
```
3. Visualize the collected prettified data on a map using the Google Maps JavaScript API. More specifically, the file (index.html) reads the most recent data in where.js to get the data to be visualized and then we use some HTML and JavaScript to actually put the data on a Google Map. You can access the result here: https://hoshinoyutaka.github.io/geoload_assignment/
