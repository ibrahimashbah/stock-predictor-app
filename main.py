from os import rename
import streamlit as st
from datetime import date
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
import pandas as pd
from plotly import graph_objs as go

st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #3886f7;">
  <a class="navbar-brand" href="https://youtube.com/dataprofessor" target="_blank">Ibrahim Ashbah</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
      <li class="nav-item active">
        <a class="nav-link" href="http://ibrahimashbah.de/" target="_blank">Home</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="https://www.linkedin.com/in/ibrahim-al-ashbah/" target="_blank">LinkedIn</a>
    </ul>
  </div>
</nav>
""", unsafe_allow_html=True)

START = "2018-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

# Page configration details
st.set_page_config(
    page_title="SPP",
    page_icon="📈",
   
)

# Header elements
st.header("Stock Price Predictor")
st.write("Hi, Watch my [30 second video](http://youtube.com/) to understand how it works, Credit by [Ibrahim Ashbah](http://ibrahimashbah.de/)")
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
    stock_change_percentage = abs(
        stock_change)/tickerData.info['previousClose']*100
    if stock_change < 0:
        stock_change_percentage = 0-stock_change_percentage
    st.metric("Current Price",
              "$" + format(tickerData.info['currentPrice']), '{:.2f}'.format(stock_change_percentage)+"%")

    st.markdown("")

    # adjust number of years
    n_years = st.slider("Years of prediction", 1, 4)
    period = n_years * 365


with col2:

    @ st.cache(allow_output_mutation=True)
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
