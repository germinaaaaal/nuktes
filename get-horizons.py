import datetime
import urllib3
from progress.bar import IncrementalBar

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

def getstars(date=None):
    # This will be to get more precise placements
    """
    now = datetime.datetime.now()

    date = "{}-{}-{} {}:{}".format(now.year, now.month, now.day, now.hour, now.minute)
    print(now.isoformat())

    nowtomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
    print("now.tomorrow: ", nowtomorrow.isoformat())
    """
    bar = IncrementalBar("Extracting...", max=len(planet_codes))

    # Get current date and time
    time_today = datetime.datetime.now()
    date_today = datetime.date.today().isoformat()
    format_time_today = "{}:{}".format(time_today.hour, time_today.minute)
    # Get date and time in 23h and 59m
    time_tomorrow = datetime.datetime.now() - datetime.timedelta(minutes=1)
    date_tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
    format_time_tomorrow = "{}:{}".format(time_tomorrow.hour, time_tomorrow.minute)

    # Fetch the html file
    http = urllib3.PoolManager()
    info = {}

    for planet in planet_codes:
        r = http.request("GET", "https://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=\
        1&COMMAND='{0}'&MAKE_EPHEM='YES'&TABLE_TYPE='OBSERVER'&START_TIME='{1} {2}'\
        &STOP_TIME='{3} {4}'&STEP_SIZE='1d'&QUANTITIES='31'&CSV_FORMAT='NO'".\
        format(planet_codes[planet], date_today, format_time_today, \
        date_tomorrow, format_time_tomorrow))

        batch = r.data.decode("utf-8").split("\n")
        #for line in batch:
        #    print(line)

        start = batch.index("$$SOE")
        end = batch.index("$$EOE")

        data = batch[start+1:end][0]
        info[planet] = data
        bar.next()

    print()
    # Separate output into usable data
    for planet in info:
        data = info[planet]
        data = data.split(" ")
        data = list(filter(None, data))
        info[planet] = data[2]
    return(info)

print(getstars())
