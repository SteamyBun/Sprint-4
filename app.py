import streamlit as st
import pandas as pd
import plotly_express as px


try:
    crashes = pd.read_csv('C:/Users/moise/Sprint-4/crashdata2021-present.csv', sep=',')
except:
    crashes = pd.read_csv('/etc/secrets/crashdata2021-present.csv', sep=',')

#changing CrashDateTime to datetime data type
crashes['CrashDateTime'] = pd.to_datetime(crashes['CrashDateTime'], format='%m/%d/%Y %H:%M')

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

st.header('crash injuries and fatalities through out the years')
crashes['CrashYear'] = crashes['CrashDateTime'].dt.year
fig_3 = px.scatter(crashes, x='CrashYear', y=['MinorInjuries', 'ModerateInjuries', 'SevereInjuries', 'FatalInjuries'], title='Injuries by Year')
st.write(fig_3)