# Crawl the UNAIDS website to scrape National AIDS Spending Assessment (NASA) reports submitted by countries in the form of country reports.

# identify word counts in these documents related to areas of interest outlined by UNAIDS by topic. Topics will include key populations and community-led response. Each of these topics will have a list of words associated with it, and each report that is scraped (excluding the non-English documents) will generate a count of the mention of each of these words. This program and its findings will be sent to my summer internship manager at UNAIDS headquarters in Geneva. They will use these findings to focus on underperforming countries.

# The data source I intend to use is the UNAIDS database of NASA eeports found at https://www.unaids.org/en/dataanalysis/knowyourresponse/nasacountryreports). Because I will be ‘Crawling [and scraping] multiple pages in a site I haven’t used before’, this will receive a Challenge Score of 8.

# I plan to use plotly to display both a map and a graph of the countries and their corresponding word-use rates. The intent is to tell the users the countries that appear (based simply on word counts) to be most closely aligned with the key words identified by UNAIDS as important points of focus. It may also make sense to represent them as a percentage of overall words or word combinations in order to ensure I am capturing useful information. Non-English reports will be excluded. For example, if one country writes rather short reports, then it makes sense that they would have a lower word count. I am still exploring this aspect of how to make the data generated as meaningful as possible; Any suggestions are greatly appreciated.


import requests
import json
from bs4 import BeautifulSoup
import re
import os
import urllib
import sqlite3
import csv
import pandas as pd
import numpy as np
import string
# import nltk
# import pprint
import pycountry
# import plotly.graph_objs as go
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from os import path
import matplotlib.pyplot as plt

COMDB = 'com.db' # defining database for community information scraped from UNAIDS
COUNTRIESJSON = 'countries.json' #defining database for country table

# setting up cache
CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

def make_request_using_cache(url):
    unique_ident = url

    if unique_ident in CACHE_DICTION:
        # print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    else:
        # print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0'}) #so we don't get blocked
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

#initiating database connection to populate tables with scraped info
def init_db():

    conn = sqlite3.connect(COMDB) #opens a connection
    cur = conn.cursor()

    statement = '''
        DROP TABLE IF EXISTS 'Countries';
    '''
    cur.execute(statement)

    statement = '''
        CREATE TABLE 'Countries'(
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Alpha2' TEXT,
            'Alpha3' TEXT,
            'EnglishName' TEXT,
            'Region' TEXT,
            'Subregion' TEXT,
            'Population' INTEGER,
            'Area' REAL
        );
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Stories';
    '''
    cur.execute(statement)

    statement = '''
        CREATE TABLE 'Stories' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Title' TEXT,
            'Contents' TEXT
        );
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Mentions';
    '''
    cur.execute(statement)

    statement = '''
        CREATE TABLE 'Mentions'(
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Country' TEXT,
            'Mentions' INTEGER,
            FOREIGN KEY(Country) REFERENCES Countries(EnglishName)
        );
    '''
    cur.execute(statement)

    conn.commit()
    conn.close()

init_db() initiates database - creates empty tables

# scrapes the first page for links to news articles, crawls to those links and scrapes article title, date, and content
def scrape_unaids():
    country_mention_count = {}
    url = 'https://www.unaids.org/en/topic/community/stories'
    baseurl = 'https://www.unaids.org'
    user_agent = {'User-agent': 'Mozilla/5.0'}
    html = make_request_using_cache(url)
    soup = BeautifulSoup(html,'html.parser')

# scraping link to article contents
    page_divs_community_response = soup.find_all(class_='inner')
    for story in page_divs_community_response:
        link_end = story.find('a')['href']
        link = baseurl + link_end

        news_html = make_request_using_cache(link) # following link to article content
        news_soup = BeautifulSoup(news_html,'html.parser')
        story_title_div = news_soup.find_all('h3')
        for st in story_title_div:
            if st.name == 'h3':
                story_title = st.text

        story_content_div = news_soup.find_all(class_='body')
        for story in story_content_div:
            paragraph_content = story.find_all('p')
            for item in paragraph_content:
                paragraph_text = item.get_text()
                for country in pycountry.countries:
                    if country.name in paragraph_text:
                        country_name = country.name
                        if country_name in paragraph_text:
                            if country_name in country_mention_count:
                                country_mention_count[country_name] += 1
                            else:
                                country_mention_count[country_name] = 1
                        # print(country.name)
                    else:
                        pass

    return country_mention_count

scrape_unaids()
# print(len(result))

def scrape_unaids_words():
    article_words = {}
    url = 'https://www.unaids.org/en/topic/community/stories'
    baseurl = 'https://www.unaids.org'
    user_agent = {'User-agent': 'Mozilla/5.0'}
    html = make_request_using_cache(url)
    soup = BeautifulSoup(html,'html.parser')

# scraping link to article contents
    page_divs_community_response = soup.find_all(class_='inner')
    for story in page_divs_community_response:
        link_end = story.find('a')['href']
        link = baseurl + link_end

        news_html = make_request_using_cache(link) # following link to article content
        news_soup = BeautifulSoup(news_html,'html.parser')
        story_title_div = news_soup.find_all('h3')
        for st in story_title_div:
            if st.name == 'h3':
                story_title = st.text
                # print(story_title) # prints each article title (102)

        story_content_div = news_soup.find_all(class_='body')
        for story in story_content_div:
            paragraph_content = story.find_all('p')
            for item in paragraph_content:
                paragraph_text = item.get_text()

                # print(paragraph_text) # prints all text content of the article (102)

        article_words[story_title] = paragraph_text
    # print(article_words) #title: contents
    # print(type(article_words)) #dictionary
    return article_words

scrape_unaids_words()

#inserting scrape for mention data and countries data into the tables
def insert_table_data(country_mention_count):
    conn = sqlite3.connect(COMDB)
    cur = conn.cursor()

    with open(COUNTRIESJSON,'r', encoding = 'utf8') as countries:

        json_file = json.load(countries)

        for row in json_file:
            Alpha2 = row['alpha2Code']
            Alpha3 = row['alpha3Code']
            EnglishName = row['name']
            Region = row['region']
            Subregion = row['subregion']
            Population = row['population']
            Area = row['area']

            insertion = (None, Alpha2, Alpha3, EnglishName, Region, Subregion, Population, Area)

            statement = 'INSERT INTO "Countries" '
            statement += 'VALUES (?,?,?,?,?,?,?,?)'

            cur.execute(statement,insertion)

    conn.commit()

    for country in country_mention_count:
        country = country
        mentions = country_mention_count[country]
        insertion = (None, country, mentions)
        statement = 'INSERT INTO "Mentions"'
        statement += 'VALUES (?,?,?)'

        cur.execute(statement, insertion)

    conn.commit()
    conn.close()


insert_table_data(scrape_unaids()) #populates countries and mentions table

#inserting scrape and countries data into the tables
def insert_table_words(article_words):
    conn = sqlite3.connect(COMDB)
    cur = conn.cursor()

    for article in article_words:
        title = article
        contents = article_words[article]
        insertion = (None, title, contents)
        statement = 'INSERT INTO "Stories"'
        statement += 'VALUES (?,?,?)'

        cur.execute(statement, insertion)

    conn.commit()
    conn.close()

insert_table_words(scrape_unaids_words()) # populates stories table


def plot_mention_freq(): #template taken from plot.ly

    conn = sqlite3.connect(COMDB)
    df = pd.read_sql_query('SELECT DISTINCT mentions, country, Alpha3 from Mentions JOIN Countries ON Mentions.Country = Countries.EnglishName;', conn)

    fig = go.Figure(data=go.Choropleth(
        locations = df['Alpha3'],
        z = df['Mentions'].astype(float),
        text = df['Country'],
        colorscale = 'Blues',
        autocolorscale=False,
        reversescale=True,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        # colorbar_tickprefix = '$',
        colorbar_title = 'Articles Mentioning Country',
        ))

    fig.update_layout(
        title_text='UNAIDS Stories about Community Responses to HIV <br> Number of Unique Articles Mentioning Country',
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        ),
        annotations = [dict(
            x=0.55,
            y=0.1,
            xref='paper',
            yref='paper',
            text='Source: <a href="https://www.unaids.org/en/topic/community/stories">\
                UNAIDS</a>',
            showarrow = False
        )]
    )

    fig.show()

def plot_mention_pop(): #template taken from plot.ly

    conn = sqlite3.connect(COMDB)
    df = pd.read_sql_query('SELECT DISTINCT mentions, country, Alpha3, Population, Area FROM Mentions JOIN Countries ON Mentions.Country = Countries.EnglishName;', conn)

    fig = go.Figure(data=go.Scatter(x=df['Population'],
                                    y=df['Mentions'],
                                    mode='markers',
                                    marker=dict(
                                    size = 10,
                                    color=df['Area'],
                                    colorscale='Viridis',
                                    showscale=True
                                    ),
                                    text=df['Country'])) # hover text goes here

    fig.update_layout(title='UNAIDS Articles Count by Population <br> Colored by Area', xaxis_title = 'Country Population', yaxis_title = 'Country Articles')
    fig.show()

def pie_chart(country_or_region):
    conn = sqlite3.connect(COMDB)
    df = pd.read_sql_query('SELECT DISTINCT mentions, country, Alpha3, Region, Area FROM Mentions JOIN Countries ON Mentions.Country = Countries.EnglishName;', conn)
    #.sort_values('Mentions')

    labels = df[country_or_region]
    values = df['Mentions']

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title='UNAIDS Articles Count by Region')
    fig.show()

# pie_chart("Country")
# pie_chart() #plots pie chart for representation by region

def word_cloud():
    conn = sqlite3.connect(COMDB)
    df = pd.read_sql_query('SELECT Contents FROM Stories;', conn)

    # text = df.Contents[0] #creates wordcloud for a single article
    text = " ".join(review for review in df.Contents)
    stopwords = set(STOPWORDS)
    # stopwords.update(["sample", "Sample2"])

    wordcloud = WordCloud(max_words=50, background_color = 'white').generate(text)

    plt.imshow(wordcloud, interpolation = 'bilinear')
    plt.axis('off')
    plt.show()

# word_cloud() #displays the most frequently mentioned words for all articles

def menu():
    help_text = 'Welcome to my Final Project. I have created a program to scrape articles related to community-led response on the UNAIDS website.\n\n' '\tYou can explore this data using the following commands:\n' "\n\tmap\n" "\t\tDisplays a map of the world color-coded by volume of articles mentioning the country\n" "\n\tscatter\n" "\t\tDisplays a scatter plot comparing a country article volume to the country population\n" "\n\twordcloud\n" "\t\tDisplays a WordCloud of the most frequently used words in UNAIDS community articles\n" "\n\tpie\n" "\t\tDisplays a pie chart of % of articles mentioning countries in each Region\n" "\n\texit\n" "\t\texits the program\n" "\n\thelp\n" "\t\tlists available commands (these instructions)\n"
    print(help_text)
    start = input("Enter a command (or 'help' for options)")
    if start == 'help':
        menu()
    elif start == 'map':
        plot_mention_freq()
        menu()
    elif start == 'scatter':
        plot_mention_pop()
        menu()
    elif start == 'wordcloud':
        word_cloud()
        menu()
    elif start == 'pie':
        pie_chart('Region')
        menu()
    elif start =='exit':
        pass
    else:
        print('invalid input, please try again')
        menu()


if __name__=="__main__":
    menu()


#     init_db()
#     scrape_unaids()
#     insert_table_data()
#     plot_mention_freq()
#     plot_mention_pop()
    # two_axes_plot()
