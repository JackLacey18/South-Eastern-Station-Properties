# PROPERTIES LOCAL TO RAILWAY STATIONS ON THE SOUTH-EASTERN NETWORK

The aim of this script is to scrape all properties listed on Rightmove (a popular housing website) within 3 miles of a 
train station on the South-Eastern railway network in the south of England. The properties will range from £100,000 to £350,000 and will try to
exclude retirement properties and shared ownership schemes that are specifically listed on the website as such.

Firstly the script will scrape all stations listed on the railway network. This information will be found on Wikipedia.
Rightmove has a unique set of characters within the URL that direct the user to a specific location. The script finds and scrapes all
area codes for each station that will be used for the scraping of properties later on. These area codes are written to a text file with the
name of each station. This script will run if that file is not already in the same folder as the script.
This file is called Station_Data.txt.

Commute times from each station will be important when considering where to buy. So the script gathers commute times from each station to
London Bridge. Google maps with Selenium is used to collect all commute times if people were to start their commute on the next working day
at 6:30am. The data was written again to a text file and only initiated if the file doesn't already exist.
This file is called Commute_Times.txt.

When we finally have all this data, we can then scrape properties listed within a 3 mile radius of each station with the stations scraped and
the area codes of each station.

Once all the properties for each station have been scraped, the script appends the commute time of each property to the listing, cleans the data
and writes the data to a CSV file called Rightmove_South-Eastern_Station_Properties_DATA_TIME.csv, date and time being the date and time the file
was written.
