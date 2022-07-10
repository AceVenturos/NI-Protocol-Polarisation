"""
Author: Jamie McKeown (Academic: jmckeown35@qub.ac.uk)

Extracts Referenced Tweets IDs from JSON file containing NI Protocol tweet data from initial Full-Archive Search
"""

import json

# List to store referenced tweet IDs
ref_tweet_ids = []

# Extract Tweet IDs for all referenced tweets, accounting for tweets which reference more than a single tweet
for line in open('NIProtocol_Dataset/niprotocol.json', 'r'):
    tweet = json.loads(line)
    if tweet['referenced_tweets'] is not None:
        for ref_tweet in tweet['referenced_tweets']:
            ref_tweet_ids.append(ref_tweet['id'])

print(str(len(ref_tweet_ids)) + " referenced tweets found")

# Remove any duplicates: https://www.w3schools.com/python/python_howto_remove_duplicates.asp
ref_tweet_ids = list(dict.fromkeys(ref_tweet_ids))
print(str(len(ref_tweet_ids)) + " tweets remaining after duplicates removed")

# Save to simple .txt file
with open('NIProtocol_Dataset/referenced_tweet_ids.txt', 'w+') as file:
    for ref_tweet_id in ref_tweet_ids:
        # Write each ID on a new line
        file.write("%s\n" % ref_tweet_id)

file.close()
