import datetime
import urllib3
from bs4 import BeautifulSoup

# Get current time
now = datetime.datetime.now()
date = "{}-{}-{}".format(now.year, now.month, now.day)
print(date)

# Curate JPL-Horizons request

# Fetch the html file
http = urllib3.PoolManager()
r = http.request("GET", "https://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=1&COMMAND='499'&MAKE_EPHEM='YES'&TABLE_TYPE='OBSERVER'&START_TIME='2000-01-01'&STOP_TIME='2000-12-31'&STEP_SIZE='15%20d'&QUANTITIES='1,9,20,23,24'&CSV_FORMAT='YES'")

batch = r.data.decode("utf-8").split("\n")

start = batch.index("$$SOE")
end = batch.index("$$EOE")

data = batch[start+1:end]
for line in data:
    print(line)

# Parse the html file
#soup = BeautifulSoup(html_doc, 'html.parser')

# Format the parsed html file
#strhtm = soup.prettify()

# Print the first few characters
#print (strhtm[:225])
