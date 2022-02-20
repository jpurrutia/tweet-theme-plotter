import tweepy
from datetime import datetime
import pandas as pd
import os
import re
from my_stop_words import stop_words
import config
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px
from flask import Flask
import dash

CONSUMER_KEY = config.CONSUMER_KEY
CONSUMER_SECRET = config.CONSUMER_SECRET
ACCESS_TOKEN = config.ACCESS_TOKEN
ACCESS_SECRET = config.ACCESS_SECRET



def auth():
    """
    Connect To Your Twitter Account via Twitter API
    """
    try:
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        api = tweepy.API(auth)
    except:
        print('Error: Authentication Failed')
    
    return api

def search_tweets(api):
    """
    Search Tweets in user_name's timeline

    Params:
        api: tweepy.API object
    """
    tweets = tweepy.Cursor(api.user_timeline, screen_name='@'+user_name).items()
    list_tweets = [tweet for tweet in tweets]

    return list_tweets 

def clean_tweets(list_tweets):
    """
    Clean Tweets and return a list of words

    Params:
        list_tweets: list of tweets
    """
    tweets_list = []

    for tweet in list_tweets:
        text = tweet.text.lower()
        text = re.sub("@[A-Za-z0-9_]+","", text)
        temp = re.sub("#[A-Za-z0-9_]+","", text)
        text = re.sub(r"http\S+", "", text)
        text = re.sub(r"www.\S+", "", text)
        text = re.sub('[()!?]', ' ', text)
        text = re.sub('\[.*?\]',' ', text)
        text = re.sub("'", "", text)
        text = re.sub("[^a-z0-9]"," ", text)            
        tweets_list.extend(text.split())

    return tweets_list


def filter_stop_words(temp_words, stop_words):
    """
    Filter Stop Words from a list of words

    Params:
        temp_words: list of words from tweets
        stop_words: list of stop words
    """
    new_list = []
    tweets_list = [word for word in temp_words if not word in stop_words]
    new_list.extend(word for word in tweets_list)

    return new_list


def get_word_counts(cleaned_list):
    """
    Get Word Counts from a list of words
    """
    word_counts = {}
    for word in cleaned_list:
        word_counts[word] = word_counts.get(word, 0) + 1
    return word_counts

def get_largest_word(word_counts):
    bigcount = None
    bigword = None
    for word, count in word_counts.items():
        if bigcount is None or count > bigcount:
            bigword = word
            bigcount = count

    
    return bigword, bigcount


def create_tweets_df(word_counts_dict, minimum_count):
    df = pd.DataFrame(word_counts_dict.items(), columns=['Word', 'Count'])
    #df = df[df['Count'] > minimum_count].sort_values(by='Count', ascending=False)
    
    return df

server = Flask(__name__)
app = dash.Dash(server=server, external_stylesheets=[dbc.themes.FLATLY])
app.title = 'Dashboard'


app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H2("What are you Tweeting?"), width={'size': 12, 'offset': 0, 'order': 0}), style = {'textAlign': 'center', 'paddingBottom': '1%'}),
    dbc.Row(dbc.Col(html.H5("Input the threshold for number of times you have tweeted about something."))),
    dcc.Input(
            id="value_input",
            type='number',
            value=1,
        ),
    dcc.Graph(id='bar-chart')
    ])
 
@app.callback(
Output("bar-chart", "figure"),
[Input("value_input", "value")])
def update_figure(minimum_count):
    df = pd.read_csv('output.csv')
    df = df[df['Count'] > minimum_count].sort_values(by='Count', ascending=False)
    fig = px.bar(df, x='Word', y='Count')
 
    return fig


if __name__ == '__main__':
    user_name = ''
    api = auth()
    tweets_list = search_tweets(api)
    tweets_list = clean_tweets(tweets_list)
    filtered_tweets = filter_stop_words(tweets_list, stop_words)
    word_counts = get_word_counts(filtered_tweets)
    df = create_tweets_df(word_counts, 5)
    dir_path = os.getcwd()
    out_path = os.path.join(dir_path, 'output.csv')
    df.to_csv(out_path)
    app.run_server(debug=True)