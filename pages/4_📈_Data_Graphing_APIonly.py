import sys
import streamlit as st
import datetime
import pandas as pd

import ea_api_request as eaapi
from plotly import figure_factory
import plotly.express as px

st.set_page_config(layout='wide')

#set globals for form attributes
station_value = 0
station_label =0
measure_values = 0
date_range = []
start_date =""
end_date =""
data_label = ""
csv=""

@st.cache_data
def getstations():
   stations_df = eaapi.get_stations()
   return stations_df
      
def getmeasures():
      df_measures =  eaapi.get_measures_station(station_id)
      return df_measures

def convert_df(df):
   return df.to_csv().encode('utf-8')


def plot():

   df_data = eaapi.get_readings_api(measure)
   df_data = df_data.sort_values(by='dateTime')

   df_data['dateTime'] = pd.to_datetime(df_data['dateTime'])
   df_data['measure'] = station_label
   df_data['type'] = data_label

   st.session_state.measure_data = pd.concat([df_data,st.session_state.measure_data])

   fig = px.line(st.session_state.measure_data, x="dateTime", y="value",title=f'Graph of selected measures grouped by type coloured by station', color="measure", facet_row="type", width=1180, height =820)
   fig.update_layout(autotypenumbers='convert types')
   fig.update_yaxes(matches=None)

   #st.write(st.session_state.measures_list)

   st.write(fig)

   csv = convert_df(df_data)

with st.expander('Guide'):
   st.markdown("""# Graph data from multiple data types from multiple sites
   - Select a station in the sidebar and the details will refresh automatically
   - Then, select the measure to get data from below
   - Repeat the selection of sites and measures as desired
   - The graphs will temporarily dissappear after selecting another station.
   - If the graph shows plotting issues clear cached data in the sidebar and build them again
   - You can export the full graphed datasets in the sidebar 
   - The charts are fully interative, you may zoom pan and toggle the data""")

stations_df = getstations()

if "measures_list" not in st.session_state:
    st.session_state.measures_list= []

if "measure_data" not in st.session_state:
   st.session_state.measure_data = pd.DataFrame()

station_lables = stations_df['label']+" "+stations_df['stationReference']

options = list(range(len(station_lables)))

if "station_value" not in st.session_state:
   st.session_state.station_value = 0

with st.sidebar.form(key='form1', clear_on_submit=False):
    st.write("Select a station and get details to see the measures recorded")
    station_value = st.selectbox("Station", options, format_func=lambda x: station_lables[x], key="station_value")
    station_label = station_lables[station_value]
    station_id = stations_df['stationReference'][station_value]

    update_measures = st.form_submit_button("Update Measures")

    df_measures = getmeasures()
    #st.write(df_measures.head())

    df_measures['Label'] = df_measures['parameterName'] + " " + df_measures['qualifier'] + " " + df_measures['valueType']
    measure_labels = df_measures['Label'].tolist()
    measure_checkboxes = st.multiselect("Select measures", measure_labels)

    date_range = st.date_input("Select a data range to view data from and to (inclusive)", (datetime.date(2022, 8, 1),datetime.date.today()))

    
    add_to_graph = st.form_submit_button("Add to Graph")

if update_measures:
    df_measures = getmeasures()
    df_measures['Label'] = df_measures['parameterName'] + " " + df_measures['qualifier'] + " " + df_measures['valueType']
    measure_labels = df_measures['Label'].tolist()
    measure_checkboxes = st.multiselect("Select measures", measure_labels)

if add_to_graph:
    start_date = date_range[0].isoformat()
    end_date = date_range[1].isoformat()

    for measure_checkbox in measure_checkboxes:
        measure_value = measure_labels.index(measure_checkbox)
        measure = df_measures['notation'][measure_value]
        data_label = measure_labels[measure_value]
        plot()


st.sidebar.download_button(
   "Press to Download",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
)

if st.sidebar.button("Clear Data Cache"):
   st.session_state.measure_data = pd.DataFrame()
