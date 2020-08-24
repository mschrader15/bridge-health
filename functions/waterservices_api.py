import requests
from datetime import datetime, timedelta
from dateutil.parser import parse
import copy

VARIABLE_CODE = {'Gage height, ft': '00065', 'Streamflow, ft&#179;/s': '00060'}


def get_url(sites, parameters, begin=None):

    params = ",".join(parameters)
    site = ",".join(sites)
    if begin:
        return f'https://waterservices.usgs.gov/nwis/iv/?sites={site}&parameterCd={params}&format=json&startDT={begin}'
    else:
        return f'https://waterservices.usgs.gov/nwis/iv/?sites={site}&parameterCd={params}&format=json'


def get_data(sites, parameters, delta_days=None):
    return_list = []
    return_dict = {param: {'measurement': None, 'time': None, 'name': None} for param in parameters}
    start_date = None
    if delta_days:
        now = datetime.now()
        start_dt = now - timedelta(days=delta_days)
        start_date = start_dt.strftime('%Y-%m-%dT%H:%M')
    r = requests.get(get_url(sites, parameters=[VARIABLE_CODE[param] for param in parameters], begin=start_date))
    raw_data = r.json()

    for j, _ in enumerate(sites):
    # it is returned in reverse order
        for i, _ in enumerate(parameters):
            return_dict[parameters[len(parameters) - (i + 1)]]['measurement'] = \
                [float(data['value']) for data in raw_data['value']['timeSeries'][i+j]['values'][0]['value']]
            return_dict[parameters[len(parameters) - (i + 1)]]['time'] = \
                [parse(data['dateTime']) for data in raw_data['value']['timeSeries'][i+j]['values'][0]['value']]
            return_dict[parameters[len(parameters) - (i + 1)]]['name'] = \
                raw_data['value']['timeSeries'][i+j]['sourceInfo']['siteName']
            return_list.append(copy.deepcopy(return_dict))
    return_list.reverse()
    return return_list


def get_lat_lon(site):
    url = f'https://waterservices.usgs.gov/nwis/iv/?sites={site}&format=json'
    r = requests.get(url)
    data = r.json()
    lat = data['value']['timeSeries'][0]['sourceInfo']['geoLocation']['geogLocation']['latitude']
    lon = data['value']['timeSeries'][0]['sourceInfo']['geoLocation']['geogLocation']['longitude']
    return lat, lon


if __name__ == "__main__":

    get_data('06935550', parameters=['Gage height, ft', 'Streamflow, ft&#179;/s'],
             delta_days=3)