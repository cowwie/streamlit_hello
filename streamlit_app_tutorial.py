import pandas as pd
import streamlit as st
import plotly.express as px
import time
from sqlalchemy import create_engine

# Define MySQL connection details
mysql_config = {
    'dialect': 'mysql',
    'host': '3.221.113.63',
    'port': 3306,
    'database': 'helloesp32',
    'username': 'root',
    'password': '!uE:Z5zgF9Ae'
}

# Create a SQLAlchemy engine
engine = create_engine(f"{mysql_config['dialect']}://{mysql_config['username']}:{mysql_config['password']}@{mysql_config['host']}:{mysql_config['port']}/{mysql_config['database']}")

st.set_page_config(
    page_title="AWS MySQL Testing",
    page_icon="XX",
    layout="wide",
)

st.title("Here is my weather app!")
st.header("Live Data")

# Function to fetch and process data
def fetch_and_process_data():
    # Fetch data from the database using SQLAlchemy
    query = "SELECT tempF, humidity, date_add(time_stamp, INTERVAL-5 HOUR) as ts FROM esp32_dht20 ORDER BY time_stamp DESC LIMIT 5760;"
    data = pd.read_sql(query, engine)

    # Extract relevant information
    current_temp = data.at[0, "tempF"]
    current_humidity = data.at[0, "humidity"]

    # Extract timestamp information
    timestamp = data.at[0, "ts"]
    lasttime_str = f"Time of Last Data: {timestamp.strftime('%m/%d/%Y at %H:%M:%S')}"

    return data, current_temp, current_humidity, lasttime_str

# Display placeholders for dynamic content
datadisplay = st.empty()    # top row
temp_graph = st.empty()     # line chart of temp
humid_graph = st.empty()    # line of humidity

while True:
    # Fetch and process data
    data, current_temp, current_humidity, lasttime_str = fetch_and_process_data()

    # Display information
    with datadisplay.container():
        st.text(lasttime_str)

        kpi1, kpi2 = st.columns(2)
        kpi1.metric(
            label="Temperature F",
            value=f"{current_temp} F",
        )
        kpi2.metric(
            label="Humidity",
            value=f"{current_humidity} %",
        )

    with temp_graph:
        fig_t = px.line(
            data,
            x="ts",
            y="tempF",
            title="Temperature (F)"
        )
        st.plotly_chart(fig_t)

    with humid_graph:
        fig_h = px.area(
            data,
            x="ts",
            y="humidity",
            title="Humidity (%)"
        )
        st.plotly_chart(fig_h)

    # Wait for 2 seconds before updating again
    time.sleep(2)