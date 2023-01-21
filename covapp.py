import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.subplots as sp
import locale
locale.setlocale(locale.LC_ALL, '')


# Read the data
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
df = pd.read_csv(url)
models= pd.read_csv("Models.csv")
# Create the header and background
st.set_page_config(page_title="COVID-19 Dashboard", page_icon=":guardsman:", layout="wide")


# st.image("RBI-Emblem-PNG.png", use_column_width=False, width=100, caption="Department of Economic and Policy Research - Division of International Finance")
st.sidebar.image("RBI-Emblem-PNG.png", use_column_width=False, width=80)
st.sidebar.markdown("Department of Economic and Policy Research - Division of International Finance")

st.title('COVID-19 Dashboard')

#Filter data for location World
world_data = df.loc[df['location'] == "World"]
world_total_cases = world_data["total_cases"].sum()

#Filter data for location United States
us_data = df.loc[df['location'] == "United States"]
us_total_cases = us_data["total_cases"].sum()

#Filter data for location India
india_data = df.loc[df['location'] == "India"]
india_total_cases = india_data["total_cases"].sum()

#Filter data for location China
china_data = df.loc[df['location'] == "China"]
china_total_cases = china_data["total_cases"].sum()

#Filter data for location World
world_data = df.loc[df['location'] == "World"]
world_total_deaths = world_data["total_deaths"].sum()

#Filter data for location United States
us_data = df.loc[df['location'] == "United States"]
us_total_deaths = us_data["total_deaths"].sum()

#Filter data for location India
india_data = df.loc[df['location'] == "India"]
india_total_deaths = india_data["total_deaths"].sum()

#Filter data for location China
china_data = df.loc[df['location'] == "China"]
china_total_deaths = china_data["total_deaths"].sum()

#Filter data for location World
world_data = df.loc[df['location'] == "World"]
world_total_vaccination = world_data["people_fully_vaccinated"].sum()

#Filter data for location United States
us_data = df.loc[df['location'] == "United States"]
us_total_vaccination = us_data["people_fully_vaccinated"].sum()

#Filter data for location India
india_data = df.loc[df['location'] == "India"]
india_total_vaccination = india_data["people_fully_vaccinated"].sum()

#Filter data for location China
china_data = df.loc[df['location'] == "China"]
china_total_vaccination = china_data["people_fully_vaccinated"].sum()


col1, col2, col3 = st.columns(3)
with col1:
        st.write("Total Cases as of 21st Jan 2023: ")
        st.write("World :",locale.format("%d", world_total_cases, grouping=True))
        st.write("United States :",locale.format("%d", us_total_cases, grouping=True))
        st.write("India :",locale.format("%d", india_total_cases, grouping=True))
        st.write("China :",locale.format("%d", china_total_cases, grouping=True))

with col2:
    st.write("Total Deaths as of 21st Jan 2023: ")
    st.write("World :",locale.format("%d", world_total_deaths, grouping=True))
    st.write("United States :",locale.format("%d", us_total_deaths, grouping=True))
    st.write("India :",locale.format("%d", india_total_deaths, grouping=True))
    st.write("China :",locale.format("%d", china_total_deaths, grouping=True))

with col3:
    st.write("Total Vaccinations as of 21st Jan 2023: ")
    st.write("World :",locale.format("%d", world_total_vaccination, grouping=True))
    st.write("United States :",locale.format("%d", us_total_vaccination, grouping=True),": 67%")
    st.write("India :",locale.format("%d", india_total_vaccination, grouping=True),": 67%")
    st.write("China :",locale.format("%d", china_total_vaccination, grouping=True)," : 89%")


# st.sidebar.empty()
# st.sidebar.image("RBI-Emblem-PNG.png", use_column_width=False, width=80)
# st.sidebar.markdown("Department of Economic and Policy Research - Division of International Finance")

location = st.sidebar.selectbox("Select a location", df["location"].unique())



# Filter the data based on the selected location
data = df[df["location"] == location]

# Show a data table for the selected location
st.dataframe(data)


fig = sp.make_subplots(rows=1, cols=3, subplot_titles=("New Cases 7D MA","New Deaths 7D MA","Stringency Index"))
# 7-day moving average of new cases
data['new_cases_ma'] = data['new_cases'].rolling(window=7).mean()

# 7-day moving average of new deaths
data['new_deaths_ma'] = data['new_deaths'].rolling(window=7).mean()

# Add new cases plot
fig.add_trace(go.Scatter(x=data['date'], y=data['new_cases_ma'], mode='lines+markers', name='New Cases 7D MA'),1,1)

# Add new deaths plot
fig.add_trace(go.Scatter(x=data['date'], y=data['new_deaths_ma'], mode='lines+markers', name='New Deaths 7D MA'),1,2)

# Add stringency index plot
fig.add_trace(go.Scatter(x=data['date'], y=data['stringency_index'], mode='lines+markers', name='Stringency Index'),1,3)

# Customize layout
fig.update_layout(title='COVID-19 Data', xaxis_title='Date', yaxis_title='Value', margin=dict(l=50, r=50, b=50, t=50, pad=4),
                 width=1200, height=400)

# Show plot
st.plotly_chart(fig)

st.bar_chart(models.set_index('Agency')['Death Forecasted'])
