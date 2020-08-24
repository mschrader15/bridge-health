import requests
from datetime import datetime
from index import config
from dateutil.parser import parse

KEY = "f0ba75a422b9742251ae12ae17c0e027"
AVOID_PART = 'minutely'


def get_url(lat, lon, part, key):
    return f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&appid={key}"


def get_future_precipitation(latitude, longitude):

    r = requests.get(get_url(latitude, longitude, AVOID_PART, config.OPENWEATHER_KEY))
    raw_data = r.json()
    hour_rain = []
    hour_time = []
    for hour_data in raw_data['hourly']:
        try:
            hour_rain.append(hour_data['rain']['1h'])
            hour_time.append(datetime.fromtimestamp(hour_data['dt']))
        except KeyError:
            continue
    day_rain = []
    day_time = []
    for day_data in raw_data['daily']:
        try:
            day_rain.append(day_data['rain'])
            day_time.append(datetime.fromtimestamp(day_data['dt']))
        except KeyError:
            continue
    return hour_time, day_time, hour_rain, day_rain


if __name__ == "__main__":

    r = get_future_precipitation(38.79744, -90.467333, AVOID_PART, KEY)
    r.json()