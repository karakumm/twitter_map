## Twitter friends map
This program creates a map of user's twitter friends' locations. 

## Usage
In order to use this program you should have bearer token to get access to Twitter API. 
You can run the program on http://karakum.pythonanywhere.com/ 

## How does it work
Twitter map program consists of one module main.py. 
There are five functions:
- users_info() to get information about twitter friends
- get_coords() to get user's locations' coordinates
- create_map() to create a map
- index() and twitter_map() works with Flask

The example of a generated map:
![Map](map.png?raw=true "output_map")
