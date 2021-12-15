import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime
from datetime import timedelta
from matplotlib import cm
import plotly.express as px

st.write("""# Welcome to first Data Science Web App """)
st.set_option('deprecation.showPyplotGlobalUse', False)


# function to show the plot

#fig, ax = plt.subplots()
#ax.scatter([1, 2, 3], [1, 2, 3])

#st.pyplot(fig)

uber = pd.read_csv('https://uberbucket12.s3.ap-south-1.amazonaws.com/UberDataset.csv', delimiter=None)
#uber = pd.read_csv('UberDataset1.csv', delimiter=None)

st.table(uber.head(5))
uber.isnull().sum().sort_values(ascending=False)

uber.rename(columns={'Date/Time':'date_time'}, inplace=True)

# Library for manipulating dates and times


# Function to convert features to datetime
def convert_date(df, cols):
  for col in cols:
    df[col] = df[col].astype(str).apply(lambda x:x.replace(' +0000 UTC', ''))
    df[col] = pd.to_datetime(df[col])
  return df

# Applying date_convertion function to date features                                     # our dates features are in object data types, 
uber = convert_date(uber, ['date_time'])

uber['year'] = uber.date_time.map(lambda x: datetime.strftime(x,"%Y"))
uber['month'] = uber.date_time.map(lambda x: datetime.strftime(x,"%b"))               # Now, let’s break down <request_time> feature 
uber['weekday'] = uber.date_time.map(lambda x: datetime.strftime(x,"%a"))             # into different date parts.
uber['time'] = uber.date_time.map(lambda x: datetime.strftime(x,"%H:%M"))
#st.write((uber['year']+'   '+uber['month']+'   '+uber['weekday']+'   '+uber['time']))

week_day = uber.pivot_table(index=['weekday'], values='Base', aggfunc='count')          # No. of Location Travelled by Customer on Particular Day of Week
week_day.head()                                                                         # for the Base Location Available

#Module 1
st.write(""" # MODULE I : HOW MANY TRIPS UBER COMPLETED OVER THE MONTHS OF 2014 """)
fig = plt.figure()
sns.scatterplot(x='month',y='Base',data=uber);
st.pyplot(fig)


form = st.form(key='my_form')
months = form.multiselect("Please select Month", ['Jan','Feb','March','Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep','Oct','Nov','Dec'])
submit = form.form_submit_button(label='OK')
if submit:
    st.write(months)    
    st.write("Total Completed Trips : ", uber.weekday.count())
    st.write(uber.month.value_counts().sort_index(ascending=True))
    moduleI = plt.figure()
    sns.countplot(data=uber, x='month',order=months, palette='bright')
    st.pyplot(moduleI)


#Module 2
st.write(""" # MODULE II :  Total Number Of Rides for The Weekdays for Each Individual Month """)

daily_rides = uber.groupby(['month','weekday'])['Base'].count()
daily_rides = daily_rides.reset_index()
daily_rides.head()

fig = plt.figure(figsize=(12,6))
sns.set_style('darkgrid')

ax = sns.pointplot(x="weekday", y="Base", hue="month", data=daily_rides)
handles,labels = ax.get_legend_handles_labels()

ax.set_xlabel('Day of Week', fontsize = 15)
ax.set_ylabel('Total Uber Pickups', fontsize = 15)
ax.set_title('Total Number of Pickups for Each Weekday per Month (April-September 2014)', fontsize=16)
ax.tick_params(labelsize = 8)
ax.legend(handles,labels,loc=0, title='Months', prop={'size':10})
ax.get_legend().get_title().set_fontsize('8')
st.pyplot(fig)


#Module 3
st.write(""" # MODULE III : Count The Rides For Every Hour Of Everyday In The Month """)
uber['time'] =  uber['date_time'].dt.time
uber['hour'] = uber['date_time'].dt.hour
uber.head()

hourly_ride = uber.groupby(['month','hour','weekday'])['Base'].count()
hourly_ride = hourly_ride.reset_index()
hourly_ride = hourly_ride.rename(columns = {'Base':'RideCount'})
hourly_ride.head()

aug_hourly_data = hourly_ride[hourly_ride.month == 'Aug']

fig = plt.figure(figsize=(12,6))
sns.set_style('darkgrid')

ax = sns.pointplot(x="hour", y="RideCount", hue="weekday", data=aug_hourly_data)
handles,labels = ax.get_legend_handles_labels()
ax.set_xlabel('Hour of Day', fontsize = 15)
ax.set_ylabel('Uber Pickups', fontsize = 15)
ax.set_title('Total Hourly Uber Pickups By Day of the Week in NYC (August 2014)', fontsize=16)
ax.tick_params(labelsize = 8)
ax.legend(handles,labels,loc=0, title="Days", prop={'size':10})
ax.get_legend().get_title().set_fontsize('8')
st.pyplot(fig)

#Module 4
st.write(""" # MODULE IV : Hourly Averages of Pickups Each Weekday """)

weekday_hourly_avg = hourly_ride.groupby(['weekday','hour'])['RideCount'].mean()
weekday_hourly_avg = weekday_hourly_avg.reset_index()
weekday_hourly_avg = weekday_hourly_avg.rename(columns = {'RideCount':'AverageRides'})
weekday_hourly_avg = weekday_hourly_avg.sort_index()
weekday_hourly_avg.head()
weekday_hourly_avg.tail()

st.table(weekday_hourly_avg.weekday.value_counts())


#Module 5
st.write(""" # MODULE V : Distribution of Uber pickups Based on the Bases""")
uber.Base.value_counts()

base_names = {"Base": {'B02617':'Weiter', 'B02598':'Hinter','B02682':'Schmecken','B02764':'Danach-NY','B02512':'Unter'}}
uber_bases = uber.copy()
uber_bases.replace(base_names, inplace=True)
st.table(uber_bases.head())
st.table(uber_bases.groupby(by=['Base']).count())
#fig= px.bar(x=uber_bases['Base'].head(5000),density=1, color='green',orientation="v",)
#st.plotly_chart(fig)


