"""
Author: Jamie McKeown (jmckoewn35@qub.ac.uk)

Adapted from Dorottya Demszky (ddemszky@stanford.edu): https://github.com/ddemszky/framing-twitter

Stream tweets based on predefined rules.
"""

import tweepy
import sys
import codecs
import json
import argparse

# TODO: argparse to allow mulitple text files to be passed plus more dynamic authentication token selection

# User arg to enable selection of specific keys and thus access
oauth = int(sys.argv[1])

# Consumer keys and access tokens, used for OAuth
# Add your list of bearer tokens
bearer_tokens = []
# Add your list of api keys
api_keys = []
# Add your list of secret api keys
api_keys_secret = []
# Add your list of access tokens
access_tokens = []
# Add your list of token secrets
access_token_secrets = []


# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(api_keys[oauth], api_keys_secret[oauth])
auth.set_access_token(access_tokens[oauth], access_token_secrets[oauth])

# Create client interface
client = tweepy.Client(bearer_token=bearer_tokens[oauth], consumer_key=api_keys[oauth],
                       consumer_secret=api_keys_secret[oauth], access_token=access_tokens[oauth],
                       access_token_secret=access_token_secrets[oauth], wait_on_rate_limit=True)


def user_to_dic(user):
    u_dic = {'id': user.id, 'name': user.name, 'username': user.username, 'location': user.location,
             'entities': user.entities, 'verified': user.verified, 'description': user.description,
             'protected': user.protected, 'pinned_tweet_id': user.pinned_tweet_id,
             'public_metrics': user.public_metrics, 'created_at': user.created_at.isoformat()}
    return u_dic


def response_to_dic(tweet, user):
    dic = {'id': tweet.id, 'text': tweet.text, 'referenced_tweets': tweet.referenced_tweets,
           'entities': tweet.entities, 'author_id': tweet.author_id, 'public_metrics': tweet.public_metrics,
           'lang': tweet.lang, 'created_at': tweet.created_at.isoformat(), 'attachments': tweet.attachments,
           'context_annotations': tweet.context_annotations, 'conversation_id': tweet.conversation_id,
           'reply_settings': tweet.reply_settings, 'geo': tweet.geo, 'user': user_to_dic(user)}
    return dic


tweet_fields = ['attachments', 'context_annotations', 'conversation_id', 'created_at', 'entities', 'geo',
                'lang', 'public_metrics', 'referenced_tweets', 'reply_settings']

user_fields = ['created_at', 'description', 'entities', 'location', 'pinned_tweet_id', 'protected', 'public_metrics',
               'verified']

expansions = ['author_id']

# TODO: Add not found tracking for deleted etc tweets

# My Essential Access, using this for testing purposes before full-on scraping
if oauth == 0:
    file = open('NIProtocol_Dataset/referenced_tweet_ids.txt')
    tweet_ids = file.read().splitlines()
    for i in range(0, len(tweet_ids), 100):
        tweets = client.get_tweets(tweet_ids[i:i + 100], tweet_fields=tweet_fields, user_fields=user_fields,
                                   expansions=expansions)
        users = {u["id"]: u for u in tweets.includes['users']}
        with codecs.open('NIProtocol_Dataset/niprotocol_extra.json', 'a', encoding='utf-8') as f:
            for tweet in tweets.data:
                if not tweet:
                    continue
                if users[tweet.author_id]:

                    # Handle Reference tweet objects - unsure if there can be more than one referenced tweets?
                    if tweet.referenced_tweets is not None:
                        referenced_tweets = []
                        for referenced_tweet in tweet.referenced_tweets:
                            referenced_tweets.append({'type': referenced_tweet.type, 'id': referenced_tweet.id})
                        tweet.referenced_tweets = referenced_tweets

                f.write(json.dumps(response_to_dic(tweet, users[tweet.author_id])) + '\n')

elif oauth == 1:
    file = open('NIProtocol_Dataset/referenced_tweet_ids.txt')
    tweet_ids = file.read().splitlines()
    for i in range(0, len(tweet_ids), 100):
        tweets = client.get_tweets(tweet_ids[i:i + 100], tweet_fields=tweet_fields, user_fields=user_fields,
                                   expansions=expansions)
        users = {u["id"]: u for u in tweets.includes['users']}
        with codecs.open('NIProtocol_Dataset/niprotocol_extra.json', 'a', encoding='utf-8') as f:
            for tweet in tweets.data:
                if not tweet:
                    continue
                if users[tweet.author_id]:

                    # Handle Reference tweet objects - unsure if there can be more than one referenced tweets?
                    if tweet.referenced_tweets is not None:
                        referenced_tweets = []
                        for referenced_tweet in tweet.referenced_tweets:
                            referenced_tweets.append({'type': referenced_tweet.type, 'id': referenced_tweet.id})
                        tweet.referenced_tweets = referenced_tweets

                f.write(json.dumps(response_to_dic(tweet, users[tweet.author_id])) + '\n')

exit(0)

