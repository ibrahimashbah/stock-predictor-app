from os import rename
import streamlit as st
from datetime import date
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
import pandas as pd

START = "2018-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

# Page configration details
st.set_page_config(
    page_title="SPP",
    page_icon="📈",
    layout="wide",
)

# Header elements
st.header("Stock Price Predictor")
st.write("watch this [30 second video](http://youtube.com/) to understand how it works, Credit by [Ibrahim Ashbah](http://ibrahimashbah.de/)")
st.markdown("____")
st.markdown("")  # Make new empty row


# Create layout of two columns
col1, col2 = st.columns((2, 2))


with col1:

    # Select Market
    selected_market = st.radio('Markets', ['Largest German companies',
                                           'S&P 500'])

    # Load Market Data
    if selected_market == "Largest German companies":
        stocks = pd.read_csv(
            'https://raw.githubusercontent.com/ibrahimashbah/stock-predictor-app/f531e6815e8aabd3bdeac8eb257ddf03b4b158cc/Largest%20German%20companies%20code.txt', header=None)
    else:
        stocks = pd.read_csv(
            'https://raw.githubusercontent.com/ibrahimashbah/stock-predictor-app/main/S%26P%20500%20index%20code.txt', header=None)

    selected_stock = st.selectbox(
        "Stock", stocks)
    st.markdown("____")

    # Ticker information
    tickerData = yf.Ticker(selected_stock)

    # Ticker current stock price
    stock_change = tickerData.info['currentPrice'] - \
        tickerData.info['previousClose']
    st.metric("Current Price",
              "$" + format(tickerData.info['currentPrice']), '{:.2f}'.format(stock_change)+"%")

    st.markdown("")

    # adjust number of years
    n_years = st.slider("Years of prediction", 1, 4)
    period = n_years * 365


with col2:

    @ st.cache(ttl=24*60*60)
    def load_data(ticker):
        data = yf.download(ticker, START, TODAY)
        data.reset_index(inplace=True)
        return data

    data = load_data(selected_stock)

    # Forecasting

    # Preparing data for model
    df_train = data[['Date', 'Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    # Training
    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)

    # Ploting
    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1, use_container_width=True)
