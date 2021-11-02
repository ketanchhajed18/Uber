import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime
from datetime import timedelta
from matplotlib import cm



st.write("""# Welcome to first Data Science Web App """)
st.set_option('deprecation.showPyplotGlobalUse', False)


# function to show the plot

#fig, ax = plt.subplots()
#ax.scatter([1, 2, 3], [1, 2, 3])

#st.pyplot(fig)

uber = pd.read_csv('https://uberbucket12.s3.ap-south-1.amazonaws.com/UberDataset.csv', delimiter=None)
st.table(uber.head(5))
uber.isnull().sum().sort_values(ascending=False)

uber.rename(columns={'Date/Time':'date_time'}, inplace=True)

# Library for manipulating dates and times


# Function to convert features to datetime
def convert_date(df, cols):
  for col in cols:
    df[col] = df[col].apply(lambda x:x.replace(' +0000 UTC', ''))
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
