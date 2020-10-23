import streamlit as st
import time
import numpy as np
import pandas as pd
import altair as alt
import datetime
import matplotlib.pyplot as plt
import mplfinance as fplt
from yahoofinancials import YahooFinancials
import matplotlib.dates as mdates
import yfinance as yf

### Initialize Variables ###
ticker_list = []
### Load Default Values into Ticker_List
ticker_list.append('TSLA')
ticker_list.append('AAPL')
start_date0 = '2020-03-01'
end_date0 = '2020-09-30'
graph_flag = 2 #default value to skip graphing routine.

#### Title and Welcome Message ####
st.title('Visualizing Stock Data')
st.write('By Adam and Bryce')
st.text("")
st.text("")
st.image('https://i.kym-cdn.com/entries/icons/original/000/029/959/Screen_Shot_2019-06-05_at_1.26.32_PM.jpg')
st.title("Introduction")
st.write("In this project we present an interactive web application for visualizing \
various aspects of investment data. By selecting an option from the drop down menu below, \
you can begin analysis of any stocks that you choose. Alternatively you can work through the \
tutorial below, which will introduce the program and highlight insights about the data.")
st.write("All data used in this project is available through the Yahoo! Finance API.")

tut_flag = st.checkbox("Show Tutorial")
if(tut_flag):
    st.title("Tutorial")
    st.write("[1] To begin this tutorial, select \"Just one for me\" from the first drop-down menu. \
    This will allow you to analyze a single stock throughout all of the graphics presented by our program.")

####################

#### User Input ####
user_choice = st.selectbox('Would you like to analyze a single stock, or compare two?',('-','Just one for me.','Let\'s do two!'))

if(user_choice == 'Just one for me.'):
    pass
    graph_flag = 0
    #st.write('Wise choice, we can always look at more later.')

    ### Tutorial Text
    if(tut_flag):
        st.write("[2] Next, choose TSLA (Tesla Motors) as your stock ticker. By default TSLA should already be selected.")

    option = st.selectbox('Which Stock Would You Like to Explore? Try some of our favorites, or choose your own!',('TSLA', 'AAPL', 'NFLX','AMZN','FB','Input My Own Ticker'))
    if(option == "Input My Own Ticker"):
        user_input = st.text_input('Input Ticker:', '')
        if(user_input):
            df = yf.download(user_input, start = start_date0, end = end_date0, progress = False)
            #Need to pull data frame for this input here.
            input_valid = 1 #default value, can change based on response of YF.
            if(df.empty):
                st.write("Invalid ticker, please enter a different one.")
            else:
                ticker_list[0] = user_input
    else:
        ticker_list[0] = option
    #debug
    #st.write("DEBUG: My choice is: " + str(ticker_list))
    if(tut_flag):
            st.write("[3] Finally, select March 1st 2020 to September 30th 2020 as your date range. These are also \
            set as the default date options.")
    start_date = st.date_input('Start Date',datetime.date(2020,3,1))
    end_date = st.date_input('End Date', datetime.date(2020,9,30))

    if(tut_flag):
        st.write("[4] When you are doing your own analysis later, you can choose any stock ticker \
        you'd like from the list we provided, or input your own. Additionally, you can select the \
        two-stock option from the first dropdown menu in order to overlay the data for two different tickers. \
        This will enable comparative analysis and could help you draw interesting conclusions!")

    #generate = st.button('Next')


### USER CHOOSES TWO ###
elif(user_choice == 'Let\'s do two!'):
    pass
    graph_flag = 1
    st.write('This should get interesting!')
    ### Choose First Stock ###
    option = st.selectbox('Choose your first stock:',('TSLA', 'AAPL', 'NFLX','AMZN','FB','Input Ticker 1'))
    if(option == "Input Ticker 1"):
        user_input = st.text_input('Input Ticker:', '')
        if(user_input):
            df = yf.download(user_input, start = start_date0, end = end_date0, progress = False)
            #Need to pull data frame for this input here.
            input_valid = 1 #default value, can change based on response of YF.
            if(df.empty):
                st.write("Invalid ticker, please enter a different one.")
            else:
                ticker_list[0] = user_input
    else:
        ticker_list[0] = option
    ### Choose Second Stock ###
    option2 = st.selectbox('Choose your second stock:',('AAPL', 'TSLA', 'NFLX','AMZN','FB','Input Ticker 2'))
    if(option2 == "Input Ticker 2"):
        user_input2 = st.text_input('Input Ticker 2:', '')
        if(user_input2 == user_input):
            st.write("You need to pick two different stocks!")
        if(user_input2):
            df = yf.download(user_input2, start = start_date0, end = end_date0, progress = False)
            #Need to pull data frame for this input here.
            input_valid = 1 #default value, can change based on response of YF.
            if(df.empty):
                st.write("Invalid ticker, please enter a different one.")
            else:
                ticker_list[1] = user_input2

        #Need to pull data frame for this input here.
        input_valid = 1 #default value, can change based on response of YF.
        if(input_valid):
            ticker_list[1] = user_input2
    else:
        ticker_list[1] = option2
    if(option2 == option):
        st.write("You need to pick two different stocks!")

    #st.write("DEBUG: My choice is: " + str(ticker_list))
    #st.write("Choose your desired date range.")
    start_date = st.date_input('Start Date',datetime.date(2020,3,1))
    end_date = st.date_input('End Date', datetime.date(2020,9,30))
    #debug
    #st.write("My choice is: " + str(ticker_list))
    ### Generate Graphics ###

    ###Input variables are:
    #start_date
    #end_date
    #ticker_list (contains tickers)
    #Fetch ticker information here.
else:
    pass

### Only display graphs if the user has chosen a selection!

if(graph_flag == 0):
    ###Pull Data
    df = yf.download(ticker_list[0], start = start_date, end = end_date, progress = False)
    df['Calendar Date'] = df.index
    df['Change Percentage'] = (df['Close']-df['Open'])/df['Open']

    st.title("Figure 1: Interactive Plot of Stock Price and Trade Volume")
    if(tut_flag):
        st.write("In this figure, we present the most basic visualization available for a stock \
        - its price. Although it is basic, this is obviously the crucial data that every investor cares \
        most about. As an interactive option, you can also hover over the data points to view the closing price, \
        percent change day-to-day, and the specific date. \
        From this first cut look at our data, it is not immediately \
        obvious if there is a clear relationship between stock price and trade volume. When you select two stocks, \
        an alternative encoding of this figure is also presented, with the ability to overlay trade volume in a different way.")
    # df = pd.DataFrame(
    # np.random.randn(200, 3),
    # columns=['a', 'b', 'c'])

    # c = alt.Chart(df.reset_index()).mark_bar().encode(
    # x = 'date', y ='Volume', tooltip=['date','Volume'], color='Volume').interactive()
    # st.write(c)

    c = alt.Chart(df.reset_index()).mark_circle().encode(
    x = 'Calendar Date', y ='Close', tooltip=['Calendar Date','Close','Change Percentage'], color='Volume', size = 'Change Percentage').interactive()
    st.altair_chart(c, use_container_width=True)
    # st.write(c)

    # a = alt.Chart(df).mark_line(opacity=1).encode(
    #     x='Date', y='Close', tooltip=['Date', 'Close']).interactive()
    # b = alt.Chart(df).mark_line(opacity=0.6).encode(
    #     x='Date', y='Volume', tooltip=['Date', 'Volume']).interactive()
    # c = alt.layer(a, b)
    # st.write(c)
    # c = alt.Chart(df).mark_line().encode(
    #     x='index', y='Close')
    # st.write(c)
    #st.altair_chart(c, use_container_width=True)

    # st.title("Figure 1: Stock Price with Total Trade Volume")
    # if(tut_flag):
    #     st.write("In this figure, we present the most basic visualization available for a stock \
    #     - its price. Although it is basic, this is obviously the crucial data that every investor cares \
    #     most about. As an interactive option, you can also overlay the daily trade volume for the stock \
    #     on this chart using the checkbox below. From this first cut look at our data, it is not immediately \
    #     obvious if there is a clear relationship between stock price and trade volume.")
    # f3b1 = st.checkbox("Fig 1. Show Trade Volume")
    #
    # fig, ax1 = plt.subplots(figsize=(8,4))
    # color = 'tab:blue'
    # ax1.plot(df.index, df.Close, label = 'Share Price',color=color)
    # if f3b1 == True:
    #     ax2 = ax1.twinx()
    #     ax2.set_ylabel("Number of Trades")
    #     color = 'tab:orange'
    #     plt.bar(df.index, df.Volume, label = 'Volume',color=color)
    #
    # ax1.legend()
    # ax1.set_title("Price of "+ticker_list[0]+ " from " +str(start_date)+ " to " +str(end_date))
    # ax1.set_ylabel("USD")
    # ax1.set_xlabel("Date")
    # st.pyplot(plt)


        ### Figure 2: Prices
        ### 4 Moving Average Check Boxes
    st.title("Figure 2: Stock Price with Simple Moving Averages")
    if(tut_flag):
        st.write("In this interactive figure, you are able to view the price of your \
        selected stock over the period of interest. In addition to the stock price, \
        you can also include plots of the ten, twenty, fifty, and one-hundred day simple \
        moving averages. A simple moving average, or SMA, is a basic calculation of asset \
        prices across several intervals, divided by the total number of intervals. In financial analysis \
        simple moving average can be used as an indicator of the health of a stock. For example, \
        when the short term SMA is greater than the long term SMA, a stock could be considered \"bullish.\"\
         Note here that if you cannot view any given SMA, you will need to expand your date range above \
         so that it can be calculated. For example, to see the 10 day moving average line, you need \
         at least 11 days of trading data in your range.")
        st.write("If you select the checkboxes for 10 Day SMA and 20 Day SMA, you can begin to study what happens \
        to stock price at these line crossing events. For example, if you study the period from mid-august to late september, \
        you can see that when the 10 Day SMA crosses the 20 day moving up, the stock price increases sharply. Inversely, when \
        the 10 day crosses the 20 day in the other direction, the stock value is generally down.")
    #st.write("DEBUG Begin Figure 2")
    f1b1 = st.checkbox("10 Day SMA")
    f1b2 = st.checkbox("20 Day SMA")
    f1b3 = st.checkbox("50 Day SMA")
    f1b4 = st.checkbox("100 Day SMA")

    rolling10 = df['Close'].rolling(window=10).mean()
    rolling20 = df['Close'].rolling(window=20).mean()
    rolling50 = df['Close'].rolling(window=50).mean()
    rolling100 = df['Close'].rolling(window=100).mean()

    fig, ax = plt.subplots(figsize=(8,4))
    ax.plot(df.index, df.Close, label = 'Price')
    if f1b1 == True:
        ax.plot(rolling10.index, rolling10.values, label = '10-days SMA')
    if f1b2 == True:
            ax.plot(rolling20.index, rolling20.values, label = '20-days SMA')
    if f1b3 == True:
            ax.plot(rolling50.index, rolling50.values, label = '50-days SMA')
    if f1b4 == True:
            ax.plot(rolling100.index, rolling100.values, label = '100-days SMA')
    ax.legend()
    ax.set_title("Price of "+ticker_list[0]+ " from " +str(start_date)+ " to " +str(end_date))
    ax.set_ylabel("USD")
    ax.set_xlabel("Date")
    st.pyplot(plt)

        ### Figure 4: Stock Prices
        ### 1 Show bollinger bands
    st.title("Figure 3: Stock Prices with Bollinger Bands")
    if(tut_flag):
        st.write("Building upon the simple moving average analysis presented in Figure 2, \"Bollinger Bands\" \
        can incorporate information about the standard deviation in order to create an upper and lower trendline. \
        In technical analysis, it is seen as a positive thing (stock will go up) if the stock price crosses the lower \
        trendline, and negative when it crosses the upper trendline. If we study the same period of time on this graph that \
        we did on the last, we will see this trend in practice. The TSLA share price skirts along the upper band until it sharply falls, \
        and then quickly recovers as it approaches the bottom band. As the price stabilizes between the bands, its potential for volatility goes down. \
        More information about Bollinger Bands can be found at: \
        https://www.investopedia.com/terms/b/bollingerbands.asp ")

    f4b1 = st.checkbox("Show Bollinger Bands")

    STD20 = df['Close'].rolling(window=20).std()
    upper_band = rolling20 + (STD20 * 2)
    lower_band = rolling20 - (STD20 * 2)

    fig, ax = plt.subplots(figsize=(8,4))
    ax.plot(df.index, df.Close, label = 'Price')
    if f4b1 == True:
        ax.plot(upper_band.index, upper_band.values, label = 'Upper Bollinger Band')
        ax.plot(lower_band.index, lower_band.values, label = 'Lower Bollinger Band')
    ax.legend()
    ax.set_title("Price of "+ticker_list[0]+ " from " +str(start_date)+ " to " +str(end_date))
    ax.set_ylabel("USD")
    ax.set_xlabel("Date")
    st.pyplot(plt)


    st.title("Figure 4: Moving Average Convergence and Divergence")
    if(tut_flag):
        st.write("The Moving Average Convergence and Divergence is a critical part of technical analysis, and this is actually something that we have used in our own trades. This is used to measure a stock's momentum, and the MACD line is compared against the signal line, which is a 9 day EMA for the MACD line. The relationship between the MACD line and the signal line will determine whether the stock is a buy, sell, or hold. For example, if the MACD is crossing the signal line from below, then the stock is a buy. If the MACD is crossing the signal line from above, then the stock is a sell. If the MACD is well above (or below) the signal line, then the stock is a hold in the current long (or short) position.")


    ShortEMA = df.Close.ewm(span=12, adjust=False).mean()
    LongEMA = df.Close.ewm(span=26, adjust=False).mean()
    MACD = ShortEMA - LongEMA
    signal = MACD.ewm(span=9, adjust=False).mean()
    # plt.figure(figsize=(12.2,4.5))
    fig, ax = plt.subplots(figsize=(8,4))
    ax.plot(df.index, MACD, label='Moving Average Convergence Divergence (MACD)', color = 'red')
    ax.plot(df.index, signal, label='Signal Line', color='blue')
    ax.legend(loc='upper left')
    ax.set_title("Moving Average Convergence and Divergence for "+ticker_list[0]+ " from " +str(start_date)+ " to " +str(end_date))
    ax.set_ylabel("USD")
    ax.set_xlabel("Date")
    st.pyplot(plt)



    st.title("Figure 5: On Balance Volume (OBV)")
    if(tut_flag):
        st.write("Examining the trade volume pattern is a critical part of technical analysis for stock trading. When a pattern is reinforced by a heavy volume, the pattern is deemed more reliable. Likewise, when a pattern is only reinforced by a weak trading volume, it is deemed less reliable. When trading volume supports a price increase, this is called convergence, but when trading volume supports a price decrease, this is called divergence. On balance volume (OBV) is particularly useful for analyzing whether or not a current trend is reinforced by popular support. For example, a stock trading low with a bullish divergence would predict that the stock would trend up. Likewise, a stock trading high with a bearish divergence would predict the stock trending down. ")

    on_balance_volume = np.where(df['Close'] > df['Close'].shift(1), df['Volume'],
    np.where(df['Close'] < df['Close'].shift(1), -df['Volume'], 0)).cumsum()
    fig, ax = plt.subplots(figsize=(8,4))
    ax.bar(df.index, df.Volume, label = 'Volume',color='orange')
    ax.plot(df.index,on_balance_volume)
    st.pyplot(plt)


    st.title("Figure 6: Candlestick Chart")
    if(tut_flag):
        st.write("Candlesticks are a form of chart that visualize a stock's open, high, low, \
        and close for a given day. In the chart below, the body of the candlestick is colored \
        red when the stock closed lower than it opened, and green when it closed higher. Candlesticks \
        can be read by picking out patterns that can be classified as \"bearish\" or \"bullish.\" \
        In Figure 6, you can also overlay the total trade volume of the stock to see how it corresponds to \
        the patterns in the candlesticks. More information about these patterns can be found \
        at: https://www.investopedia.com/trading/candlestick-charting-what-is-it/ . While trying to identify \
        these patterns it is also beneficial to select a smaller date range so that the candlesticks are more easily seen.")
    f2b1 = st.checkbox("Fig. 6 Show Trade Volume")

    fplt.plot(
                df,
                type='candle',
                style='charles',
                figratio=(12,8),
                # title=ticker_name + " " + start_date_human + " to " + end_date_human,
                volume=f2b1,
                figsize=(6,5),
                show_nontrading=True,
                ylabel_lower='Shares\nTraded',
                ylabel='Price ($)'
            )
    st.pyplot(plt)


if(graph_flag == 1):
    pass
    df = yf.download(ticker_list[0], start = start_date, end = end_date, progress = False)
    df2 = yf.download(ticker_list[1], start=start_date, end=end_date, progress=False)
    st.title("Figure 0a: Interactive Graph of Stock Price - " + ticker_list[0])
    df['Calendar Date'] = df.index
    df['Change Percentage'] = (df['Close']-df['Open'])/df['Open']
    c = alt.Chart(df.reset_index()).mark_circle().encode(
    x = 'Calendar Date', y ='Close', tooltip=['Calendar Date','Close','Change Percentage'], color='Volume', size = 'Change Percentage').interactive()
    st.altair_chart(c, use_container_width=True)
    st.title("Figure 0b: Interactive Graph of Stock Price - " + ticker_list[1])
    df['Calendar Date'] = df2.index
    df['Change Percentage'] = (df2['Close']-df2['Open'])/df2['Open']
    c = alt.Chart(df.reset_index()).mark_circle().encode(
    x = 'Calendar Date', y ='Close', tooltip=['Calendar Date','Close','Change Percentage'], color='Volume', size = 'Change Percentage').interactive()
    st.altair_chart(c, use_container_width=True)


    # st.title("Figure 0: Interactive Graph of Stock Price")
    # df = yf.download(ticker_list[0], start = start_date, end = end_date, progress = False)
    #
    # df['Calendar Date'] = df.index
    # df['Change Percentage'] = (df['Close']-df['Open'])/df['Open']
    # df2['Calendar Date'] = df2.index
    # df2['Change Percentage'] = (df2['Close']-df2['Open'])/df2['Open']
    # a = alt.Chart(df.reset_index()).mark_circle().encode(
    # x = 'Calendar Date', y ='Close', tooltip=['Calendar Date','Close','Change Percentage'], color = 'Volume', size = 'Change Percentage').interactive()
    # b = alt.Chart(df2.reset_index()).mark_circle().encode(
    # x = 'Calendar Date', y ='Close', tooltip=['Calendar Date','Close','Change Percentage'], color='Volume', size = 'Change Percentage').interactive()
    # c = alt.layer(a, b)

    ### Volume PLOT

    # a = alt.Chart(df).mark_line(opacity=1).encode(
    #     x='Date', y='Close', tooltip=['Date', 'Close']).interactive()
    # b = alt.Chart(df).mark_line(opacity=0.6).encode(
    #     x='Date', y='Volume', tooltip=['Date', 'Volume']).interactive()
    # c = alt.layer(a, b)
    # st.write(c)
    # c = alt.Chart(df).mark_line().encode(
    #     x='index', y='Close')
    # st.write(c)
    #st.altair_chart(c, use_container_width=True)

    st.title("Figure 1: Stock Price with Total Trade Volume")
    f3b1 = st.checkbox("Fig 1. Show Trade Volume")
    df_vol_avg = df.Volume.mean()
    df2_vol_avg = df2.Volume.mean()

    fig, ax1 = plt.subplots(figsize=(8,4))
    ax1.plot(df.index, df.Close, label = (ticker_list[0]+' Price'),color='blue')
    ax1.plot(df2.index, df2.Close, label = (ticker_list[1]+' Price'),color='orange')
    if f3b1 == True:
        ax2 = ax1.twinx()
        ax2.legend(loc = 'lower left')
        ax2.set_ylabel("Total Trades")
        if df_vol_avg > df2_vol_avg:
            plt.bar(df.index, df.Volume, label=(ticker_list[0]+' Volume'), color='purple')
            plt.bar(df2.index, df2.Volume, label=(ticker_list[1]+' Volume'), color='yellow')
        else:
            plt.bar(df2.index, df2.Volume, label=(ticker_list[1]+' Volume'), color='yellow')
            plt.bar(df.index, df.Volume, label=(ticker_list[0]+' Volume'), color='purple')
    ax1.legend(loc = 'upper left')
    ax1.set_ylabel("USD")
    ax1.set_xlabel("Date")
    st.pyplot(plt)



    ###SMA Plot ###
    st.title("Figure 2: Stock Price with Simple Moving Averages")

    f1b1 = st.checkbox("10 Day SMA")
    f1b2 = st.checkbox("20 Day SMA")
    f1b3 = st.checkbox("50 Day SMA")
    f1b4 = st.checkbox("100 Day SMA")

    rolling10 = df['Close'].rolling(window=10).mean()
    rolling20 = df['Close'].rolling(window=20).mean()
    rolling50 = df['Close'].rolling(window=50).mean()
    rolling100 = df['Close'].rolling(window=100).mean()
    rolling10_2 = df2['Close'].rolling(window=10).mean()
    rolling20_2 = df2['Close'].rolling(window=20).mean()
    rolling50_2 = df2['Close'].rolling(window=50).mean()
    rolling100_2 = df2['Close'].rolling(window=100).mean()

    fig, ax1 = plt.subplots(figsize=(8, 4))
    ax1.plot(df.index, df.Close, label=(ticker_list[0]+' Price'),color='cyan')
    ax2 = ax1.twinx()
    ax2.plot(df2.index, df2.Close, label=(ticker_list[1]+' Price'),color='magenta')
    if f1b1 == True:
        ax1.plot(rolling10.index, rolling10.values, label='10-days SMA', color = 'red')
        ax2.plot(rolling10_2.index, rolling10_2.values, label='10-days SMA', color = 'green')
    if f1b2 == True:
        ax1.plot(rolling20.index, rolling20.values, label='20-days SMA', color = 'orange')
        ax2.plot(rolling20_2.index, rolling20_2.values, label='20-days SMA', color = 'blue')
    if f1b3 == True:
        ax1.plot(rolling50.index, rolling50.values, label='50-days SMA', color = 'yellow')
        ax2.plot(rolling50_2.index, rolling50_2.values, label='50-days SMA', color = 'purple')
    if f1b4 == True:
        ax1.plot(rolling100.index, rolling100.values, label='100-days SMA', color = 'brown')
        ax2.plot(rolling100_2.index, rolling100_2.values, label='100-days SMA', color = 'gray')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    st.pyplot(plt)


    ## BOLLINGER
    st.title("Figure 3: Stock Prices with Bollinger Bands")

    f4b1 = st.checkbox("Show Bollinger Bands")
    STD20 = df['Close'].rolling(window=20).std()
    upper_band = rolling20 + (STD20 * 2)
    lower_band = rolling20 - (STD20 * 2)

    STD20_2 = df2['Close'].rolling(window=20).std()
    upper_band_2 = rolling20_2 + (STD20_2 * 2)
    lower_band_2 = rolling20_2 - (STD20_2 * 2)

    fig, ax1 = plt.subplots(figsize=(8, 4))
    ax1.plot(df.index, df.Close, label=(ticker_list[0]+' Price'), color = 'blue')
    ax2 = ax1.twinx()
    ax2.plot(df2.index, df2.Close, label=(ticker_list[1]+' Price'), color = 'black')
    if f4b1 == True:
        ax1.plot(upper_band.index, upper_band.values, label='Upper Bollinger Band', color = 'orange')
        ax1.plot(lower_band.index, lower_band.values, label='Lower Bollinger Band', color = 'orange')
        ax2.plot(upper_band_2.index, upper_band_2.values, label='Upper Bollinger Band', color = 'red')
        ax2.plot(lower_band_2.index, lower_band_2.values, label='Lower Bollinger Band', color = 'red')
    ax1.legend(loc = 'upper left')
    ax2.legend(loc = 'upper right')
    ax1.set_ylabel("USD")
    ax1.set_xlabel("Date")
    ax2.set_ylabel("USD")
    st.pyplot(plt)


    ### MACD ###
    st.title("Figure 4: Moving Average Convergence and Divergence")

    ShortEMA = df.Close.ewm(span=12, adjust=False).mean()
    LongEMA = df.Close.ewm(span=26, adjust=False).mean()
    MACD = ShortEMA - LongEMA
    signal = MACD.ewm(span=9, adjust=False).mean()
    ShortEMA_2 = df2.Close.ewm(span=12, adjust=False).mean()
    LongEMA_2 = df2.Close.ewm(span=26, adjust=False).mean()
    MACD_2 = ShortEMA_2 - LongEMA_2
    signal_2 = MACD_2.ewm(span=9, adjust=False).mean()
    fig, ax1 = plt.subplots(figsize=(8, 4))
    ax1.plot(df.index, MACD, label=(ticker_list[0]+' MACD'), color = 'orange')
    ax1.plot(df.index, signal, label='Signal Line', color='blue')
    ax2 = ax1.twinx()
    ax2.plot(df2.index, MACD_2, label=(ticker_list[1]+' MACD'), color = 'red')
    ax2.plot(df2.index, signal_2, label='Signal Line', color='black')
    ax1.legend(loc='upper left')
    ax2.legend(loc='lower left')
    ax1.set_xlabel("Date")
    st.pyplot(plt)

    #####################
    # ON BALANCE VOLUME #
    #####################
    st.title("Figure 5: On Balance Volume (OBV)")

    on_balance_volume = np.where(df['Close'] > df['Close'].shift(1), df['Volume'],
    np.where(df['Close'] < df['Close'].shift(1), -df['Volume'], 0)).cumsum()
    on_balance_volume_2 = np.where(df2['Close'] > df2['Close'].shift(1), df2['Volume'],
    np.where(df2['Close'] < df2['Close'].shift(1), -df2['Volume'], 0)).cumsum()
    fig, ax1 = plt.subplots(figsize=(8, 4))
    ax1.bar(df.index, df.Volume, label = (ticker_list[0]+' Volume'),color='orange')
    ax1.plot(df.index,on_balance_volume,label =(ticker_list[0]+' OBV'), color = 'blue')
    ax2 = ax1.twinx()
    ax2.bar(df2.index, df2.Volume, label = (ticker_list[1]+' Volume'),color='red')
    ax2.plot(df2.index,on_balance_volume_2,label =(ticker_list[1]+' OBV'), color = 'black')
    ax1.legend(loc='upper left')
    ax2.legend(loc='lower left')
    st.pyplot(plt)

references = st.checkbox('Show References')

if(references):
	st.title('References')
	st.write('[1] 	Title: How to check if the string is empty.')
	st.write('		URL: https://stackoverflow.com/questions/9573244/how-to-check-if-the-string-is-empty')
	st.write('		Description: We used this website to learn how to determine if a string is empty.')
	st.write('[2] 	Title: Moving Average Convergence Divergence (MACD)')
	st.write('		URL: https://www.investopedia.com/terms/m/macd.asp')
	st.write('		Description: We used this website to learn about the MACD technical statisuct for measuring stocks.')
	st.write('[3] 	Title: Developing your Fist Streamlit App.')
	st.write('		URL: https://medium.com/swlh/streamlit-quickly-build-a-web-app-using-python-1afe3db4d552')
	st.write('		Description: We used this website to learn how to use Streamlit.')
	st.write('[4] 	Title: How to calculate moving average using NumPy')
	st.write('		URL: https://stackoverflow.com/questions/14313510/how-to-calculate-moving-average-using-numpy')
	st.write('		Description: We used this website to learn how to plot moving averages using Python.')
	st.write('[5] 	Title: Technical Analysis Bollinger Bands with Python')
	st.write('		URL: https://codingandfun.com/bollinger-bands-pyt/')
	st.write('		Description: We used this website to learn how to plot Bollinger Bands with Python.')
	st.write('[6] 	Title: Using Python to Visualize Stock Data " to Candlestick Charts')
	st.write('		URL: https://towardsdatascience.com/using-python-to-visualize-stock-data-to-candlestick-charts-e1a5b08c8e9c')
	st.write('		Description: We used this website to learn how to plot candlesticks with Python.')
	st.write('[7] 	Title: A comprehensive guide to downloading stock prices in Python')
	st.write('		URL: https://towardsdatascience.com/a-comprehensive-guide-to-downloading-stock-prices-in-python-2cd93ff821d4')
	st.write('		Description: We used this to learn how to download Yahoo Finance data.')
