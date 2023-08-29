import json

import pandas as pd
import requests
import numpy as np

import db_utils2 as db_utils2


def get_stations():
    r = requests.get('http://environment.data.gov.uk/flood-monitoring/id/stations?_limit=10000')

   

    data = r.json()

    df = pd.json_normalize(data, record_path=["items"]).drop(['measures'], axis=1)
    df = df.replace(np.nan, 0)
    df.replace('Nan', 'Blank')
    return df 

def get_measures_station(station):
    r = requests.get(f"http://environment.data.gov.uk/flood-monitoring/id/measures?stationReference={station}")

 
    data = r.json()

    df = pd.json_normalize(data, record_path=["items"])


    return df 



def get_readings_sql(measure,start_date,end_date):

    
    con = db_utils2.db_connect()

    cur = con.cursor()
    
    cur.execute(f"""ATTACH DATABASE the_database_path AS database2""")

    cur.execute(f"""PRAGMA cache_size = -128000""")

    df = pd.read_sql_query(f"""SELECT * from "values" WHERE measure = '{measure}'  AND 
                          datetime(dateTime) >= datetime({start_date})
                         AND datetime(dateTime) <= datetime({end_date}) """, con)

    cur.close()

    return df 
df_stations = get_stations()


def get_readings_api(measure):
    r = requests.get(f"http://environment.data.gov.uk/flood-monitoring/id/measures/{measure}/readings")
    data = r.json()

    df = pd.json_normalize(data, record_path=["items"])


    return df 

#  df = pd.read_sql_query(f"""SELECT * from readings WHERE measure='{measure}'   AND 
#                          datetime(date_time) >= datetime({start_date})
#                         AND datetime(date_time) <= datetime({end_date}) """, con)



