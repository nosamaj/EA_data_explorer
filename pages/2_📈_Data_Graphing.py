import plotly.express as px
import sys
import streamlit as st

import ea_api_request as eaapi


stations_df = eaapi.get_stations()

station_lables = stations_df['label']

options = list(range(len(station_lables)))

value = st.selectbox("gender", options, format_func=lambda x: station_lables[x])

#station_selection = st.selectbox('Which station should we view?', station_lables)

st.write(f"{value}")

station_id = stations_df['@id'][value]

st.write(f"{station_id}")


df_measures =  eaapi.get_measures_station(stations_df['@id'][value])



