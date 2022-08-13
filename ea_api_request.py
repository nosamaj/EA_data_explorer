import json

import pandas as pd
import requests

import db_utils


def get_stations():
    r = requests.get('https://environment.data.gov.uk/flood-monitoring/id/stations?_limit=10000')

   

    data = r.json()

    df = pd.json_normalize(data, record_path=["items"]).drop(['measures'], axis=1)

    return df 

def get_measures_station(station):
    r = requests.get(f"http://environment.data.gov.uk/flood-monitoring/id/measures?stationReference={station}")

 
    data = r.json()

    df = pd.json_normalize(data, record_path=["items"])


    return df 

def get_readings_sql(measure,start_date,end_date):

    
    con = db_utils.db_connect()

    cur = con.cursor()

    df = pd.read_sql_query(f"""SELECT * from all_readings WHERE measure='{measure}'   AND 
                          datetime(dateTime) >= datetime({start_date})
                         AND datetime(dateTime) <= datetime({end_date}) """, con)

    cur.close()

    return df 
df_stations = get_stations()

#df_stations.head()

df_measures = get_measures_station(df_stations['stationReference'][173])

#df_measures.head()

df_results.head()


print(df_measures["@id"][0])

df_results = get_readings_sql(measure = df_measures["@id"][0], start_date="'2022-04-09T02:00:00Z'", end_date="'2022-04-09T03:00:00Z'")

df_results.head(10)



