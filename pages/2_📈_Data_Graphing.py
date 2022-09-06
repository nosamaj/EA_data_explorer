import plotly.express as px
import sys
import streamlit as st
import datetime
import pandas as pd

import ea_api_request as eaapi
from plotly import figure_factory
import plotly.express as px


stations_df = eaapi.get_stations()

station_lables = stations_df['label']

options = list(range(len(station_lables)))

value = st.sidebar.selectbox("Station", options, format_func=lambda x: station_lables[x])

#station_selection = st.selectbox('Which station should we view?', station_lables)

#st.write(f"{value}")

station_id = stations_df['stationReference'][value]

#st.write(f"{station_id}")


df_measures =  eaapi.get_measures_station(station_id)

st.write(df_measures.head())

df_measures['Label'] = df_measures['parameterName']+" "+df_measures['qualifier'] +" "+df_measures['valueType']


measure_lables = df_measures['Label']


options2 = list(range(len(measure_lables)))

value2 = st.sidebar.selectbox("measurement", options2, format_func=lambda x:measure_lables[x])

date_range= st.sidebar.date_input(
     "Select a data range to view data from and to (00:00 to 00:00)",
     (datetime.date(2022, 8, 1),datetime.date.today())
     )#

st.write(date_range)

df_data = eaapi.get_readings_sql(measure=df_measures['@id'][value2],start_date="'2022-03-09T02:00:00Z'", end_date="'2022-03-17T03:00:00Z'")
df_data = df_data.sort_values(by='dateTime')

df_data['dateTime'] = pd.to_datetime(df_data['dateTime'])

fig = px.line(df_data, x="dateTime", y="value",title = station_id)
fig.update_layout(autotypenumbers='convert types')

st.write(fig)