import streamlit as st
import time
import numpy as np
import pandas as pd
import altair as alt
import datetime
import matplotlib.pyplot as plt

### Initialize Variables ###
ticker_list = ['TSLA', 'AAPL', 'NFLX','AMZN','FB']

#### Title and Welcome Message ####
st.title('Visualizing Stock Data')
st.write('By Adam and Bryce')
####################

#### User Input ####
option = st.selectbox('Which Stock Would You Like to Explore? Try some of our favorites, or choose your own!',('TSLA', 'AAPL', 'NFLX','AMZN','FB','Input My Own Ticker'))

if(option == 'Input My Own Ticker'):
    user_input = st.text_input('Input Ticker:', '')

    #Need to pull data frame for this input here.
    input_valid = 1 #default value, can change based on response of YF.
    if(input_valid):
        ticker_list.append(user_input)

st.write(ticker_list)
