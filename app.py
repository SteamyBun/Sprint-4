import streamlit as st
import pandas as pd
import plotly_express as px

crashes = pd.read_csv('C:\\Users\\moise\\OneDrive\\Documents\\GitHub\\Sprint-4\\crashdata2011-2020.csv', sep=',')

# getting rid of unnecessary columns
columns_to_drop = ['Name', 'TcrNumber', 'ProximityToIntersection', 'DirectionFromIntersection', 'Comment', 'ShortFormFlag', 'Distance', 'PedestrianDirectionFrom', 'PedestrianDirectionTo']
crashes = crashes.drop(columns_to_drop, axis=1)

#changing CrashDateTime to datetime data type
crashes['CrashDateTime'] = pd.to_datetime(crashes['CrashDateTime'], format='%m/%d/%Y %H:%M')

st.header('Crashes in San Jose(2011-2020)')
st.dataframe(crashes)

st.header('Crashes by hour of day and month')
crashes['hour'] = pd.to_datetime(crashes['CrashDateTime']).dt.hour
fig = px.histogram(crashes, x="hour", nbins=24, title="Crashes by Hour of Day")
fig_month = px.histogram(crashes, x="CrashDateTime", nbins=30, title="Crashes by Month")
show_month = st.checkbox('Show crashes by month')
if show_month:
    st.plotly_chart(fig_month)
else:
    st.plotly_chart(fig)