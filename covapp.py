import streamlit as st
import pandas as pd

import plotly.graph_objs as go
import plotly.graph_objects as go
import plotly.subplots as sp
import plotly.express as px
from datetime import datetime
import locale




locale.setlocale(locale.LC_ALL, '')


# Read the data
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
df = pd.read_csv(url)
models= pd.read_csv("Models.csv")
variant= pd.read_csv("OmicronVar.csv")
china= pd.read_csv("VariantsinChina.csv")
vaccinebycompany= pd.read_csv("VaccinebyMan.csv")
efficacy= pd.read_csv("Vaccine Efficacy.csv")
policy= pd.read_csv("Policy.csv")
export= pd.read_csv("Vaccine export.csv")
# Create the header and background
st.set_page_config(page_title="COVID-19 Dashboard", page_icon=":guardsman:", layout="wide")


# st.image("RBI-Emblem-PNG.png", use_column_width=False, width=100, caption="Department of Economic and Policy Research - Division of International Finance")
st.sidebar.image("RBI-Emblem-PNG.png", use_column_width=False, width=80)
st.sidebar.markdown("Department of Economic and Policy Research - Division of International Finance")

st.title('COVID-19 Dashboard')
st.write("The data on the coronavirus pandemic is updated daily")

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
        st.write("Total Cases as of : ",datetime.today().strftime('%Y-%m-%d'))
        st.write("World :",locale.format("%d", world_total_cases, grouping=True))
        st.write("United States :",locale.format("%d", us_total_cases, grouping=True))
        st.write("India :",locale.format("%d", india_total_cases, grouping=True))
        st.write("China :",locale.format("%d", china_total_cases, grouping=True))

with col2:
    st.write("Total Deaths as of : ",datetime.today().strftime('%Y-%m-%d'))
    st.write("World :",locale.format("%d", world_total_deaths, grouping=True))
    st.write("United States :",locale.format("%d", us_total_deaths, grouping=True))
    st.write("India :",locale.format("%d", india_total_deaths, grouping=True))
    st.write("China :",locale.format("%d", china_total_deaths, grouping=True))

with col3:
    st.write("Total Vaccinations as of : ",datetime.today().strftime('%Y-%m-%d'))
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


fig = sp.make_subplots(rows=1, cols=3, subplot_titles=(f"New Cases 7D MA for {location}",f"New Deaths 7D MA for {location}",f"Stringency Index for {location}"))
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
fig.add_shape(
    type='line',
    x0='2021-01-01', y0=data['new_cases_ma'].min(), x1='2021-01-01', y1=data['new_cases_ma'].max(),
    line=dict(color='yellow', width=1, dash='dot')
)
fig.add_shape(
    type='line',
    x0='2022-10-10', y0=data['new_cases_ma'].min(), x1='2022-10-10', y1=data['new_cases_ma'].max(),
    line=dict(color='yellow', width=1, dash='dot')
)
fig.add_annotation(
    x='2021-01-01', y=data['new_cases_ma'].max(),
    text='Delta',
    showarrow=True,
    font=dict(
        color='white',
        size=14
    ),
    align='center'
)
fig.add_annotation(
    x='2022-10-10', y=data['new_cases_ma'].max(),
    text='Omicron',
    showarrow=True,
    font=dict(
        color='white',
        size=14
    ),
    align='center'
)

# Show plot
st.plotly_chart(fig)


#Filter data for the selected countries
filtered_data = variant[variant["Country"].isin(["Australia", "France", "India", "South Korea", "Japan", "USA"])]


col4, col5 = st.columns(2)
with col4:
       fig = go.Figure([go.Bar(x=models["Agency"], y=models['Death Forecasted'],marker_color='yellow',marker_line_width=1)])
       fig.update_layout(width=500, height=400,title_text='Forecasted Deaths in China by Various Agnecies')
       st.write(fig) 
       
with col5:
    fig = go.Figure([go.Bar(x=filtered_data["Country"], y=filtered_data["%Omicron GRA (B.1.1.529+BA.*) in past 4 weeks"],marker_color='orange',marker_line_width=1)])
    fig.update_layout(width=500, height=400,title_text='latest omicron BA2.75 in various countries ')
    st.write(fig) 

col6, col7 = st.columns(2)
with col6:
    fig = go.Figure(data=[go.Bar(x=china['first_seq'], y=china['num_seqs'], name=Variant,
             orientation='v',
             text=china['num_seqs'],
             textposition='auto') for Variant in china["Variant"].unique()])
    fig.update_layout(barmode='stack',title_text='Different Variants in China')
    st.write(fig)

with col7:
    fig = go.Figure(data=[
    go.Bar(name='Covaxin', x=vaccinebycompany['Covaxin'], y=vaccinebycompany['Location'], orientation='h'),
    go.Bar(name='Johnson&Johnson', x=vaccinebycompany['Johnson&Johnson'], y=vaccinebycompany['Location'], orientation='h'),
    go.Bar(name='Moderna', x=vaccinebycompany['Moderna'], y=vaccinebycompany['Location'], orientation='h'),
    go.Bar(name='Novavax', x=vaccinebycompany['Novavax'], y=vaccinebycompany['Location'], orientation='h'),
    go.Bar(name='Oxford/AstraZeneca', x=vaccinebycompany['Oxford/AstraZeneca'], y=vaccinebycompany['Location'], orientation='h'),
    go.Bar(name='Pfizer/BioNTech', x=vaccinebycompany['Pfizer/BioNTech'], y=vaccinebycompany['Location'], orientation='h'),
    go.Bar(name='Sinopharm/Beijing', x=vaccinebycompany['Sinopharm/Beijing'], y=vaccinebycompany['Location'], orientation='h'),
    go.Bar(name='Sinovac', x=vaccinebycompany['Sinovac'], y=vaccinebycompany['Location'], orientation='h'),
    go.Bar(name='Sputnik V', x=vaccinebycompany['Sputnik V'], y=vaccinebycompany['Location'], orientation='h'),])
    # Change the bar mode
    fig.update_layout(barmode='stack',xaxis_title='Total Vaccinations',yaxis_title='Location',title_text='Vaccine by Manufacturer')
    st.write(fig)




col8, col9= st.columns(2, gap="large")
with col8:
    #filter data for specific locations
   filtered_data = df[(df['date'] >= 'Jan 01, 2021') & (df['date'] <= 'Jan 23, 2023')]

   filtered_data = df[df['location'].isin(["World","India","China","United States"])]
   #Calculate 7-day moving average
   filtered_data['7_day_MA'] = filtered_data['people_fully_vaccinated'].rolling(window=7).mean()
   filtered_data.dropna()
   colors = {'World': 'lightblue', 'India': 'orange', 'China': 'green', 'United States': 'red'}
   fig = px.area(filtered_data, x='date', y='7_day_MA', color='location', color_discrete_map = colors, title="7-day moving average of people_fully_vaccinated", labels={'location':'Location'})
   fig.update_layout(
        showlegend=True,
        legend=dict(x=0, y=1)
    )
   st.write(fig)

with col9:
    
    fig = go.Figure(data=[
    go.Bar(name='Alpha', x=efficacy['Alpha'], y=efficacy['Vaccine'], orientation='h'),
    go.Bar(name='Beta', x=efficacy['Beta'], y=efficacy['Vaccine'], orientation='h'),
    go.Bar(name='Gamma', x=efficacy['Gamma'], y=efficacy['Vaccine'], orientation='h'),
    go.Bar(name='Delta', x=efficacy['Delta'], y=efficacy['Vaccine'], orientation='h'),
    go.Bar(name='BA.2/.1', x=efficacy['BA.2/.1'], y=efficacy['Vaccine'], orientation='h'),
    go.Bar(name='BA.5', x=efficacy['BA.5'], y=efficacy['Vaccine'], orientation='h'),])
    # Change the bar mode
    fig.update_layout(barmode='stack',xaxis_title='Efficiency Percentage(%)',yaxis_title='Vaccine',title_text='Vaccine Efficacy')
    st.write(fig)

col10, col11= st.columns(2)
with col10:
    st.markdown("Govt. Response to rising Chinese COVID Cases")
    st.dataframe(policy)

with col11:
    data = [go.Bar(x=export['Producing economy'],
              y=export['Exports as share of total supply'],
              marker=dict(color='rgb(55, 83, 109)'), width=0.5)]

    layout = go.Layout(title='Exports as share of total supply by Producing economy',
                   xaxis=dict(title='Producing economy'),
                   yaxis=dict(title='Exports as share of total supply'))

    fig = go.Figure(data=data, layout=layout)
    st.plotly_chart(fig)




st.write("New COVID-19 cases are falling globally, barring China.")
st.write("1. Level of stringency has moderated significantly in case of India and US whereas the recent spike in COVID cases has resulted imposition of various measures in China.")
st.write("2.China lifting its Zero-Tolerance COVID policy on December 8, 2022, and has provided an official estimate of 59,938 deaths.")
st.write("3.Official estimates seem to be significantly lower than those from other experts.")
st.write("4.Now, one larger wave is predicted as against the previous estimate of one larger and more severe wave. The large continuous wave implies increased pressure on healthcare services and therefore, potentially higher fatalities.")

st.empty()

st.markdown("Copyright \u00A9 2023 Reserve Bank of India")





hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
