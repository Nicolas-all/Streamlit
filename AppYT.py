from pandas.tseries.offsets import Hour
import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

#--------------------------------- ---------------------------------  ---------------------------------
#--------------------------------- Preparing data
#--------------------------------- ---------------------------------  ---------------------------------

da = pd.read_json(r'C:\Users\allix\Desktop\Hadoop-bi\Youtubr\watch-history.json')

da.to_csv(r'C:\Users\allix\Desktop\Hadoop-bi\Youtubr\watch-history.csv',index = None)

da = pd.read_csv(r'C:\Users\allix\Desktop\Hadoop-bi\Youtubr\watch-history.csv')

column_with_nan = da.columns[da.isnull().any()]
for column in column_with_nan:
    print(column, da[column].isnull().sum())

for column in column_with_nan:
    if da[column].isnull().sum()*100.0/da.shape[0] > 90:
            da.drop(column,1, inplace=True)

da = da[da['title'] != 'Vous avez regardé une vidéo qui a été supprimée']
da = da[da['titleUrl'] != 'NaN']
da = da[da['titleUrl'] != 'nan']

da['Time']=da['time'].map(pd.to_datetime)

def get_weekday(dt):
    return dt.weekday()
def get_dom(dt):
    return dt.day
def get_hour(dt):
    return dt.hour
def get_minute(dt):
    return dt.minute
def get_second(dt):
    return dt.second
def get_year(dt):
    return dt.year
def get_month(dt):
    return dt.month

da['weekday']=da['Time'].map(get_weekday)
da['day']=da['Time'].map(get_dom)
da['hour']=da['Time'].map(get_hour)
da['minute']=da['Time'].map(get_minute)
da['seconde']=da['Time'].map(get_second)
da['year']=da['Time'].map(get_year)
da['month']=da['Time'].map(get_month)

da.to_csv(r'C:\Users\allix\Desktop\Hadoop-bi\Streamlit\App\Data.csv')

df=pd.read_csv(r"C:\Users\allix\Desktop\Hadoop-bi\Streamlit\App\Data.csv")

#--------------------------------- ---------------------------------  ---------------------------------
#--------------------------------- Setting up the app
#--------------------------------- ---------------------------------  ---------------------------------

st.set_page_config(layout='wide')
title_image = Image.open(r"C:\Users\allix\Desktop\Hadoop-bi\Streamlit\App\YTlogo.png")
st.image(title_image)
st.title('Youtube usage evolution')
st.markdown("What data can we extract from our YouTube account ***and what can we learn about ourself ?***")
st.markdown("This project have been made in order to develop an app were I can how my usage of youtube changes over the years.")
st.markdown("The YouTube data have been find in GoogleTakeout, they start in 2012 and finish in 2022.")

#--------------------------------- ---------------------------------  ---------------------------------
#--------------------------------- Sidebar creation
#--------------------------------- ---------------------------------  ---------------------------------

st.sidebar.write("This is my Streamlit project")
st.sidebar.write("If you want to see my others projects come check my Github")
st.sidebar.write("https://github.com/Nicolas-all")
st.sidebar.write("Want to know more about me ?")
st.sidebar.write("https://www.linkedin.com/in/nicolas-allix/")

session = {"All data":"All data", 
    "Data filter per year":"Data filter per year"}
selected_db = st.sidebar.selectbox("Select view", session.values())


By_years = df.groupby('year')['year'].count()\
    .sort_values(ascending=False).index

#--------------------------------- ---------------------------------  ---------------------------------
#--------------------------------- Code for the view with filtered data per year
#--------------------------------- ---------------------------------  ---------------------------------

if selected_db == session["Data filter per year"]:

    st.markdown("### **Select a year:**")
    Select_years = []

    Select_years.append(st.selectbox('', By_years))

    nbview = df[df['year'].isin(Select_years)]

    pop = nbview.groupby('title')['year'].count()\
        .sort_values(ascending = False).index[0]

    def count_rows(rows):
        return len(rows)


    By_month = nbview.groupby(['year','month']).apply(count_rows)


    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"**Number of view:** {nbview.shape[0]}")
        st.subheader('Number of view per month')
        hist_values = np.histogram(nbview['month'],bins=12, range=(1,13))[0]
        st.line_chart(hist_values)

    with col2:
        st.markdown(f"**Most viewed:** {pop}")
        st.subheader('Repartition per day')
        hist_values2 = np.histogram(nbview['day'],bins=31, range=(1,31))[0]
        st.bar_chart(hist_values2)

    st.subheader('Top 5')
    st.write('Here are the 5 most viewed video during the year and the number of times the video has been seen')
    st.dataframe(nbview.groupby('title')['year'].count().sort_values(ascending = False)[0:5])

#--------------------------------- ---------------------------------  ---------------------------------
#--------------------------------- Code for the view with all the data
#--------------------------------- ---------------------------------  ---------------------------------

elif selected_db == session["All data"] :
    st.markdown("### **Since 2012**")

    pop = df.groupby('title')['year'].count()\
        .sort_values(ascending = False).index[0]

    def count_rows(rows):
        return len(rows)
    
    by_date = df.groupby(['year','month']).apply(count_rows)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"**Number of view:** {df.shape[0]}")
        st.subheader('Repartition through the years')
        hist_values1 = np.histogram(df['month'],bins=12, range=(1,13))[0]
        st.line_chart(hist_values1)
        

    with col2:
        st.markdown(f"**Most viewed:** {pop}")
        st.subheader('Repartition through the month')
        hist_values2 = np.histogram(df['day'],bins=31, range=(1,31))[0]
        st.bar_chart(hist_values2)

    st.subheader('Top 5')
    st.write('Here are the 5 most viewed video during the year and the number of times the video has been seen')
    st.dataframe(df.groupby('title')['year'].count().sort_values(ascending = False)[0:5])


#--------------------------------- ---------------------------------  ---------------------------------
#--------------------------------- craping test (does not work yet)
#--------------------------------- ---------------------------------  ---------------------------------

#from requests_html import HTMLSession
#from bs4 import BeautifulSoup as bs
#import requests
#import os

#session = HTMLSession()

#def get_video_info(url):
    #response = session.get(url)
    #response.html.render(sleep=1, timeout=60)
    #soup = bs(response.html.html, "html.parser")
    #result = {}

#for i in URL:
    #video_url = i
# init an HTML Session
    #session = HTMLSession()
# get the html content
    #response = session.get(video_url)
# execute Java-script
    #response.html.render(sleep=1)
# create bs object to parse HTML
    #soup = bs(response.html.html, "html.parser")
    #soup.find_all("meta")

#title = soup.find("meta", itemprop="name")['content']
#genre = soup.find("meta", itemprop="genre")['content']
#dt_publication = soup.find("meta", itemprop="datePublished")['content']
#temps = soup.find("span", {"class": "ytp-time-duration"})

#test = [title,genre,temps,dt_publication]

#for i in URL:
    #get_video_info(i)
    #print (i)

#for URL in URL:
    #def get_video_info(URL):
    # download HTML code
        #response = session.get(URL)
    # execute Javascript
        #response.html.render(sleep=1, timeout=60)
    # create beautiful soup object to parse HTML
       # soup = bs(response.html.html, "html.parser")
        #a=soup.find("meta", itemprop="name")['content']
        #return (a)