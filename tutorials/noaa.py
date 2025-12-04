import requests
import sqlite3
from datetime import datetime, timedelta
import json

# NOAA (EUA) - Gratuita
def get_noaa_tides(station_id, begin_date, end_date):
    url = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
    params = {
        'product': 'predictions',
        'application': 'NOS.COOPS.TAC.WL',
        'begin_date': begin_date,
        'end_date': end_date,
        'datum': 'MLLW',
        'station': station_id,
        'time_zone': 'lst_ldt',
        'units': 'metric',
        'interval': 'hilo',
        'format': 'json'
    }
    response = requests.get(url, params=params)
    return response.json()

print( get_noaa_tides("1630000","2025-01-16 17:41:08","2025-02-16 17:41:08"))