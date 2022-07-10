import tweepy

def user_to_dic(user):
    """
    Formats Twitter User object into a sorted dictionary - done to achieve a consistent key order when json-ifying

    :param user: Twitter user object
    :return: Sorted dictionary for the user object
    """
    u_dic = {'id': user.id, 'name': user.name, 'username': user.username, 'location': user.location,
             'entities': user.entities, 'verified': user.verified, 'description': user.description,
             'protected': user.protected, 'pinned_tweet_id': user.pinned_tweet_id,
             'public_metrics': user.public_metrics, 'created_at': user.created_at.isoformat()}
    return u_dic


def response_to_dic(tweet, user):
    """
    Formats Twitter Tweet object into a sorted dictionary - done to achieve a consistent key order when json-ifying

    :param tweet: Twitter tweet object
    :param user: Twitter user object
    :return: Sorted dictionary representing the tweet object containing a nested sorted dictionary representing the user
    object
    """
    dic = {'id': tweet.id, 'text': tweet.text, 'referenced_tweets': tweet.referenced_tweets,
           'entities': tweet.entities, 'author_id': tweet.author_id, 'public_metrics': tweet.public_metrics,
           'lang': tweet.lang, 'created_at': tweet.created_at.isoformat(), 'attachments': tweet.attachments,
           'context_annotations': tweet.context_annotations, 'conversation_id': tweet.conversation_id,
           'reply_settings': tweet.reply_settings, 'geo': tweet.geo, 'user': user_to_dic(user)}
    return dic
