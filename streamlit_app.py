import streamlit as st
#import utils.db_utils as db_utils
import ea_api_request
#import utils.fetcharchive as fetcharchive
#import utils.create_db_tables as create_db_tables
import pydeck as pdk



st.title('EA Open Data Viewer')

st.markdown('''This application will allow the user to explore the EA flooding API for
- Rainfall data from the EA Gauges
- River Level and Flow data 
- Groundwater and tide data.

The options available are to see a map of the available sites, graph data for comparision and explore a statistical analaysis of data.''')

df_stations = ea_api_request.get_stations()


    
# r = pdk.Deck(
#      map_style="light",
#      initial_view_state=pdk.ViewState(
#          latitude= 53.2,
#          longitude=-3,
#          zoom=5,
#          pitch=0,
#      ),
#      layers=[
#          pdk.Layer(
#              'ScatterplotLayer',
#              data=df_stations,
#              get_position='[long, lat]',
#              get_color='[200, 30, 0, 160]',
#              get_radius=200,
#          )
#      ]
#  )

#r.to_html("test.html", open_browser=True, notebook_display=False)

#st.pydeck_chart(r)

import leafmap.foliumap as leafmap




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