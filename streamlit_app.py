import streamlit as st
import db_utils
import ea_api_request
import fetcharchive
import create_db_tables

st.title = "EA Open Data Viewer"

st.markdown = """ This application will allow the user to explore the EA flooding API for
- Rainfall data from the EA Gauges
- River Level and Flow data 
-groundwater and tide data.

The options available are to see a map of the available sites, graph data for comparision and explore a statistical analaysis of data. """

