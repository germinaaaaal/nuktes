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
    "Pluto" : 999,
    "Eris" : 136199,
    "Ceres" : 1
}

def getstars(date=None):
    # Get current UTC date and time
    now = datetime.datetime.utcnow()
    now_format = "{}-{}-{} {}:{}".format(now.year, now.month, now.day, now.hour, now.minute)

    tomorrow = datetime.datetime.utcnow() + datetime.timedelta(days=1) # Horizons requires two dates, one for the values and another upper date
    tomorrow_format = "{}-{}-{} {}:{}".format(tomorrow.year, tomorrow.month, tomorrow.day, tomorrow.hour, tomorrow.minute)

    bar = IncrementalBar("Extracting...", max=len(planet_codes))

    # Another method to get current date and time
    """
    time_today = datetime.datetime.now()
    print(time_today)
    date_today = datetime.date.today().isoformat()
    format_time_today = "{}:{}".format(time_today.hour, time_today.minute)
    print(format_time_today)
    # Get date and time in 23h and 59m
    time_tomorrow = datetime.datetime.now() - datetime.timedelta(minutes=1)
    date_tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
    format_time_tomorrow = "{}:{}".format(time_tomorrow.hour, time_tomorrow.minute)
    """
    # Fetch the html file
    http = urllib3.PoolManager()
    info = {}

    for planet in planet_codes:
        # Format request link with current date, time, and planet
        rlink = "https://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=\
        1&COMMAND='{0}'&MAKE_EPHEM='YES'&TABLE_TYPE='OBSERVER'&START_TIME='{1}'\
        &STOP_TIME='{2}'&STEP_SIZE='1d'&QUANTITIES='31'&CSV_FORMAT='NO'".\
        format(planet_codes[planet], now_format, tomorrow_format)
        r = http.request("GET", rlink)

        batch = r.data.decode("utf-8").split("\n")

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
        info[planet] = float(data[2])
    return(info)
