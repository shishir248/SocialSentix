import pandas as pd
import json
import praw
import re
import math
import os
import ast
from wordcloud import WordCloud
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from praw.models import MoreComments

class SocialSentix:
    def __init__(self, reddit):
        self.reddit = reddit
        self.subreddit = 'all'

    def main(self):
        ticker_file = open("./tickers.txt", "r+")
        self.tickers = []
        for line in ticker_file:
            self.tickers.append(line.strip())
        self.data_fty22()
        ticker_file.close()

    def data_fty22(self):
        df = pd.read_csv('wallstreetbets_2022.csv')
        # Data cleaning
        df['body'].fillna('', inplace=True)

        # Find tickers and create new col
        df['tickers'] = df['body'].str.findall(rf'\b({"|".join(map(re.escape, self.tickers))})\b',flags=re.IGNORECASE)
        df_tickers = df.loc[df['tickers'].astype(bool)].reset_index()

        # Fetch URLs for reddit which have Nan values.
        df_tickers = self.batch_urls(df_tickers)

        # Remove dups.
        df_tickers['tickers'] = df_tickers['tickers'].apply(ast.literal_eval)
        unq_symbols = []
        for ticker in df_tickers['tickers']:
            unq = set([s.upper() for s in ticker])
            ls = list(unq)
            unq_symbols.append(ls)
            df_tickers['tickers'] = unq_symbols

        # Apply sentiments
        sentiment_score = []
        for comment in df_tickers['body']:
            score = self.run_sentiment(comment)
            sentiment_score.append(score)
        df_tickers['sentiment'] = sentiment_score

        # Prepare JSON
        symbol_json_raw = self.prepare_json(df_tickers)

        # Add wordcloud -> After this the symbol_wordlcloud is available
        self.add_wordcloud(symbol_json_raw)



    def prepare_json(self, df):
        ticker_dict = {}
        for index, row in df.iterrows():
            # Parse the tickers string into a list of tickers
            tickers = ast.literal_eval(row['tickers'])
            comments = []
            # Iterate through the tickers for this comment
            for ticker in tickers:
                # Create a comment object for this comment
                comment = {
                    'id': row['id'],
                    'url': row['url'],
                    'body': row['body'],
                    'timestamp': row['timestamp'],
                    'unix': row['created'],
                    'score': row['sentiment']
                }

                # If the ticker is not in the dictionary, add it with an empty list
                if ticker not in ticker_dict:
                    ticker_dict[ticker] = {'comments':[]}

                # Append the comment object to the ticker's list
                ticker_dict[ticker]['comments'].append(comment)

            ticker_dict_new = {}
            for t, d in ticker_dict.items():
                total_sentiment_score = 0
                total_comments = len(d['comments'])
                for comment in d['comments']:
                    total_sentiment_score += comment['score']
                avg_score = total_sentiment_score/total_comments
                ticker_dict_new.update({t: {'total_score': avg_score, 'comments': d['comments']}})

            return ticker_dict_new


    def add_wordcloud(self, data):
        output_dir = 'assets/wordcloud_images'
        os.makedirs(output_dir, exist_ok=True)

        for s,v in data.items():
            comments = ' '
            img_path = os.path.join(output_dir,f'{s}_wordcloud.png')
            for comm in v['comments'][:5]:
                comments += comm['body'] + " "
            wordcloud = WordCloud(width = 800, height=400, background_color='#8dd5f2').generate(comments)
            wordcloud.to_file(img_path)

        for s,v in data.items():
            data[s]['img_path'] = f'/assets/{s}_wordcloud.png'

        with open('./symbol_wordlcloud.json', 'w') as fp:
            json.dump(data, fp)

    def batch_urls(self, data):
        dfs = []
        max = math.ceil(len(data)/60)
        for i in range(max):
            dfs.append(data[i*60: i*60 + 60 - 1].apply(self.fetch_url, axis = 1))
        return pd.concat(dfs)

    def fetch_url(self, row):
        if pd.isna(row['url']):
            fetched_url = self.reddit.comment(row.id).permalink
            row['url'] = fetched_url
        return row

    def create_df(self):
        # Get submissions
        self.query_subreddit()

    # How to get comments live. Ignore this as we are using available dataset
    def query_subreddit(self):
        for comment in self.reddit.subreddit('wallstreetbets').stream.comments():
            cbody = comment.body
            if any(keyword in cbody for keyword in self.tickers):
                print(cbody)

    def run_sentiment(self, comment):
        analyser = SentimentIntensityAnalyzer()
        return analyser.polarity_scores(comment)['compound']

def get_credentials():
    cred_file = open('cred.json')
    creds = json.load(cred_file)
    return creds

def main():
    creds = get_credentials()
    reddit = praw.Reddit(
        client_id=creds['client_id'],
        client_secret=creds['client_secret'],
        user_agent=creds['user_agent'],
        username=creds['username'],
        password=creds['password']
    )
    socialsentix = SocialSentix(reddit)
    socialsentix.main()

main()
