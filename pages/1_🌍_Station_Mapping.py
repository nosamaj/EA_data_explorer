import streamlit as st
#import utils.db_utils as db_utils
import ea_api_request
#import utils.fetcharchive as fetcharchive
#import utils.create_db_tables as create_db_tables
import leafmap.foliumap as leafmap

st.title('EA Open Data Viewer')

st.markdown('''This application will allow the user to explore the EA flooding API for
- Rainfall data from the EA Gauges
- River Level and Flow data 
- Groundwater and tide data.

The options available are to see a map of the available sites, graph data for comparision and explore a statistical analaysis of data.''')

df_stations = ea_api_request.get_stations()

st.title("Marker Cluster")

with st.expander("See source code"):
    with st.echo():

        m = leafmap.Map(center=[54.2, -3], zoom=6)
       
        stations = df_stations

       
        m.add_points_from_xy(
            stations,
            x="long",
            y="lat",
            #color_column='catchmentName',
            icon_names=['gear', 'map', 'leaf', 'globe'],
            spin=True,
            add_legend=True
        )

m.to_streamlit(height=700)