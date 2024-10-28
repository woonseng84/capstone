import altair as alt
import pandas as pd
import streamlit as st
from utility import check_password

# Show the page title and description.
st.set_page_config(page_title="Graduate Employment Survey")
st.title("Graduate Employment Survey")

if not check_password():
    st.stop()

st.write(
    """
    This app visualizes data from "Graduate Employment Survey - NTU, NUS, SIT, SMU, SUSS & SUTD".
    It shows the emplyment rate and the gross pay of the graduate from respective local uni and school. The data is from Jan 2013 to 2022.
    This data assists prospective students to make informed course decisions.
    """
)