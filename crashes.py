import streamlit as st
import pandas as pd
import plotly_express as px
import requests
import urllib.request

#Pulling data from the website
url = 'https://data.sanjoseca.gov/api/3/action/resource_show?id=15408d78-9734-4ea1-b3e5-a0f99568dd9b'
api_key = '046095c1-4d70-4c50-8f15-d05c1ec05ffb'
response = requests.get(url, headers={'Authorization': api_key})
download_url = response.json()['result']['url']
urllib.request.urlretrieve(download_url, 'crashes.csv')
crashes = pd.read_csv('crashes.csv')

#changing CrashDateTime to datetime data type
crashes['CrashDateTime'] = pd.to_datetime(crashes['CrashDateTime'], format='%m/%d/%Y %I:%M:%S %p')

#dropping unnecessary columns
columns_to_drop = ['Name', 'TcrNumber', 'ProximityToIntersection', 'DirectionFromIntersection', 'Comment', 'ShortFormFlag', 'Distance', 'PedestrianDirectionFrom', 'PedestrianDirectionTo']
crashes = crashes.drop(columns_to_drop, axis=1)

st.header('Crashes in San Jose(2021-present)')
st.dataframe(crashes)

st.header('Crashes by hour of day and month')

#defineing first histogram showing crashes per hour of the day
crashes['CrashTime'] = crashes['CrashDateTime'].dt.hour
fig_1 = px.histogram(crashes, x="CrashTime", nbins=24, 
                   labels={'CrashDateTime': 'Time of Day', 'count': 'Crash Count'},
                   title='Histogram of Car Crashes Throughout the Day',
                   color_discrete_sequence=['darkblue'])
fig_1.update_traces(marker_line_color="black", marker_line_width=1)

#defineing the alternate histogram showing crashes per month
crashes['CrashMonth'] = crashes['CrashDateTime'].dt.month
fig_2 = px.histogram(crashes, x='CrashMonth', nbins=24,
                    labels={'CrashDateTime': 'Month', 'count': 'Crash Count'},
                    title='Histogram of Car Crashes Throughout the Months',
                    color_discrete_sequence=['darkgreen'])
fig_2.update_traces(marker_line_color="black", marker_line_width=1)

show_month = st.checkbox('Show crashes by month')

if show_month:
    st.plotly_chart(fig_2)
else:
    st.plotly_chart(fig_1)

#making scatter plot showing the change in injuries throughout the years by month
st.header('crash injuries and fatalities through out the years')
crashes['CrashYearMonth'] = crashes['CrashDateTime'].dt.to_period('M').astype(str)
fig_3 = px.scatter(crashes, x='CrashYearMonth', y=['MinorInjuries', 'ModerateInjuries', 'SevereInjuries', 'FatalInjuries'], title='Injuries by Year')
fig_3.update_layout(xaxis_title='Crash Year and Month')
st.write(fig_3)