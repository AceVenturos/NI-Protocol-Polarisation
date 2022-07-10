"""
Author: Jamie McKeown (jmckoewn35@qub.ac.uk)

Adapted from Dorottya Demszky (ddemszky@stanford.edu): https://github.com/ddemszky/framing-twitter

Stream tweets based on predefined rules.
"""

import tweepy
import sys
import codecs
import json
import time
from help_functions import response_to_dic

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



# https://github.com/twitterdev/getting-started-with-the-twitter-api-v2-for-academic-research/blob/main/modules/5-how-to-write-search-queries.md
# https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
query = '(#NIProtocol OR #NorthernIrelandProtocol OR NI Protocol OR Northern Ireland Protocol OR #AE22 OR #AE2022 OR ' \
        '#AssemblyElection22 OR #AssemblyElection2022 OR Assembly Election NI OR Assembly Election Northern Ireland) ' \
        'lang:en -is:retweet'

# Time Period is April to May 2022
start_time = '2022-04-01T00:00:00Z'
end_time = '2022-06-01T00:00:00Z'

# Utilised following page to find equvilaent field attributes from v1.1 to v2:
# https://developer.twitter.com/en/docs/twitter-api/migrate/data-formats/standard-v1-1-to-v2

# Note to self, retweeted_status.id returns the referenced tweet as an object including all of the tweet fields as normal tweets within the "includes" part of the tweet object
# text and id is returned as default
# status.is_quote_status not present in v2, is a boolean determining whether tweet is a Quoted tweet
# Within tweet fields, organic and promoted metrics exist. These are both subsets of the combined set of public and non-public metrics TODO: script recreating these for measurnig purposes potentially https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet
tweet_fields = ['attachments', 'context_annotations', 'conversation_id', 'created_at', 'entities', 'geo',
                'lang', 'public_metrics', 'referenced_tweets', 'reply_settings']

user_fields = ['created_at', 'description', 'entities', 'location', 'pinned_tweet_id', 'protected', 'public_metrics',
               'verified']

expansions = ['author_id']

data = []
includes_users = []
errors = []
meta = []

# My Essential Access, using this for testing purposes before full-on scraping
if oauth == 0:
    for page in tweepy.Paginator(client.search_recent_tweets, query=query, tweet_fields=tweet_fields,
                                 user_fields=user_fields, expansions=expansions, max_results=100, limit=10):

        tweets = tweepy.Response(data=page.data, includes=page.includes, errors=page.errors, meta=page.meta)
        users = {u["id"]: u for u in tweets.includes['users']}

        try:
            with codecs.open('NIProtocol_Dataset/niprotocol_test.json', 'a', encoding='utf-8') as f:
                for tweet in tweets.data:
                    if users[tweet.author_id]:

                        # Handle Reference tweet objects - unsure if there can be more than one referenced tweets?
                        if tweet.referenced_tweets is not None:
                            referenced_tweets = []
                            for referenced_tweet in tweet.referenced_tweets:
                                referenced_tweets.append({'type': referenced_tweet.type, 'id': referenced_tweet.id})
                            tweet.referenced_tweets = referenced_tweets

                        f.write(json.dumps(response_to_dic(tweet, users[tweet.author_id])) + '\n')
                    else:
                        print("User/Tweet Alignment Error")
                        exit(0)
        # Error handling
        except (BaseException, tweepy.TweepyException) as e:
            print("Error on_status: %s" % str(e))

elif oauth == 1:
    for page in tweepy.Paginator(client.search_all_tweets, query=query, tweet_fields=tweet_fields,
                                 user_fields=user_fields, expansions=expansions, max_results=100, start_time=start_time,
                                 end_time=end_time):
        tweets = tweepy.Response(data=page.data, includes=page.includes, errors=page.errors, meta=page.meta)
        users = {u["id"]: u for u in tweets.includes['users']}
        time.sleep(2)

        try:
            with codecs.open('NIProtocol_Dataset/niprotocol.json', 'a', encoding='utf-8') as f:
                for tweet in tweets.data:
                    if users[tweet.author_id]:

                        # Handle Reference tweet objects - unsure if there can be more than one referenced tweets?
                        if tweet.referenced_tweets is not None:
                            referenced_tweets = []
                            for referenced_tweet in tweet.referenced_tweets:
                                referenced_tweets.append({'type': referenced_tweet.type, 'id': referenced_tweet.id})
                            tweet.referenced_tweets = referenced_tweets

                        f.write(json.dumps(response_to_dic(tweet, users[tweet.author_id])) + '\n')
                    else:
                        print("User/Tweet Alignment Error")
                        exit(0)
        # Error handling
        except (BaseException, tweepy.TweepyException) as e:
            print("Error on_status: %s" % str(e))

exit(0)

