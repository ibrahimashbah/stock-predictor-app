from os import rename
import streamlit as st
from datetime import date
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
import pandas as pd
from plotly import graph_objs as go

# Page configration details
st.set_page_config(
    page_title="Stock Forecast App",
    page_icon="📈",


)
hide_st_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)
st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #3886f7;">
  <a class="navbar-brand" href="http://ibrahimashbah.de/" target="_blank">Ibrahim Ashbah</a>
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

# Title elements
st.markdown('''# **Stock Forecast App**
A stock forecast app for Largest German companies and S&P500 companies.
''')


with st.expander("What are the necessery skills to build like this app? "):
    st.write("""
                - Web Scrabing ✅
                - Data Cleaning ✅
                - Data Wrangling ✅
                - Data extraction and manuplation from Excel/SQL ✅
                - Data manipulation from large data sets ✅
                - Coding knowledge with several languages: Python, HTML/CSS, Jave ✅
                - Good mathematical, data analytics and problem solving skills ✅
                - Knowledge of advanced statistical techniques and concepts ✅
                - Analyze model performance and data accuracy ✅
                - Familiar with Machine Learning techniques, Pandas, NumPy and SciPy ✅
                - Build PowerPoint presentations to recommend business decisions ✅
        """)

with st.expander("How the model works?"):
    st.write("""
         The chart above shows some numbers I picked for you.
         I rolled actual dice for these, so they're *guaranteed* to
         be random.
     """)
    st.image("https://www.ncrypted.net/blog/wp-content/uploads/2019/02/Freemium.png")


START = "2018-01-01"
TODAY = date.today().strftime("%Y-%m-%d")


# Select Market
st.sidebar.markdown("")
st.sidebar.markdown("")

selected_market = st.sidebar.radio('Markets', ['Largest German companies',
                                               'S&P 500'])

# Load Market Data
if selected_market == "Largest German companies":
    stocks = pd.read_csv(
        'https://raw.githubusercontent.com/ibrahimashbah/stock-predictor-app/f531e6815e8aabd3bdeac8eb257ddf03b4b158cc/Largest%20German%20companies%20code.txt', header=None)
else:
    stocks = pd.read_csv(
        'https://raw.githubusercontent.com/ibrahimashbah/stock-predictor-app/main/S%26P%20500%20index%20code.txt', header=None)
st.sidebar.markdown("____")
st.sidebar.markdown("")

selected_stock = st.sidebar.selectbox(
    "Stock", stocks)

# Ticker information
tickerData = yf.Ticker(selected_stock)

# Ticker current stock price
stock_change = tickerData.info['currentPrice'] - \
    tickerData.info['previousClose']
stock_change_percentage = abs(
    stock_change)/tickerData.info['previousClose']*100
if stock_change < 0:
    stock_change_percentage = 0-stock_change_percentage

st.sidebar.markdown("")
cols_at_sidabar = st.sidebar.columns([1, 1])
with cols_at_sidabar[0]:
    string_logo = '<img src=%s>' % tickerData.info['logo_url']
    st.markdown(string_logo, unsafe_allow_html=True)
with cols_at_sidabar[-1]:
    st.metric("Current Price",
              "$" + format(tickerData.info['currentPrice']), '{:.2f}'.format(stock_change_percentage)+"%")


# adjust number of years
st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.markdown("")
n_years = st.sidebar.slider("Years of prediction", 1, 4)
period = n_years * 365

placeholder = st.empty()
placeholder.header(
    "Loading the plot...")


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
fig1.update_layout(
    xaxis_title="Date",
    yaxis_title="Price",

)
placeholder.plotly_chart(fig1, use_container_width=True)
