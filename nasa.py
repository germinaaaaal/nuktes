import datetime
import urllib3
from bs4 import BeautifulSoup

# Link planets to their Horizons code
planet_codes = {
    "Sun" : 10,
    "Mercury" : 199,
    "Venus" : 299,
    "Mars" : 499,
    "Jupiter" : 599,
    "Saturn" : 699,
    "Uranus" : 799,
    "Neptune" : 899,
    "Pluto" : 999
}

# This will be to get more precise placements
"""
now = datetime.datetime.now()

date = "{}-{}-{} {}:{}".format(now.year, now.month, now.day, now.hour, now.minute)
print(now.isoformat())

nowtomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
print("now.tomorrow: ", nowtomorrow.isoformat())
"""
# Get current date
date = datetime.date.today.isoformat()

# Fetch the html file
http = urllib3.PoolManager()

for planet in planet_codes:
    r = http.request("GET", "https://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=\
    1&COMMAND='{0}'&MAKE_EPHEM='YES'&TABLE_TYPE='OBSERVER'&START_TIME='{1} 00:0\
    0'&STOP_TIME='{1} 23:59'&STEP_SIZE='3h'&QUANTITIES='31'&CSV_FORMAT='YES'".\
    format(planet_codes[planet], date))

    batch = r.data.decode("utf-8").split("\n")
    print(batch)
    start = batch.index("$$SOE")
    end = batch.index("$$EOE")

    data = batch[start+1:end]
    for line in data:
        print(planet + " " + line)
