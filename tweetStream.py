import tweepy
import json
consumerKey = "yourConsumerKey"
consumerSecret = "yourConsumerSecret"
accessToken = "yourAccessToken"
accessTokenSecret = "yourAccesTokenSecret"

created_at = ''
tweet_text = ''
location = ''
username = '' #this is what shows on @username
userhandle = '' #this is what shows on top of tweets
favourite_count = 0
retweet_count = 0
follower_count = 0
following_count = 0
overall_tweet_count = 0
tweet_id = 0
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if status._json['lang'] == 'en': #filter by language

            print('caught')
            if 'retweeted_status' in status._json:
                if 'extended_tweet' in status._json['retweeted_status']:
                    tweet_text = status._json['retweeted_status']['extended_tweet']['full_text']
                else:
                    tweet_text = status._json['retweeted_status']['text']
                tweet_id = status._json['retweeted_status']['id']
                created_at = status._json['retweeted_status']['user']['created_at']
                username = status._json['retweeted_status']['user']['screen_name']
                userhandle = status._json['retweeted_status']['user']['name']
                location = status._json['retweeted_status']['user']['location']
                follower_count = status._json['retweeted_status']['user']['followers_count']
                following_count = status._json['retweeted_status']['user']['friends_count']
                overall_tweet_count = status._json['retweeted_status']['user']['statuses_count']
                favourite_count = status._json['retweeted_status']['favorite_count']
                retweet_count = status._json['retweeted_status']['retweet_count']
            else:
                if 'extended_tweet' in status._json:
                    tweet_text = status._json['extended_tweet']['full_text']
                else:
                    tweet_text = status._json['text']
                tweet_id = status._json['id']
                created_at = status._json['user']['created_at']
                username = status._json['user']['screen_name']
                userhandle = status._json['user']['name']
                location = status._json['user']['location']
                follower_count = status._json['user']['followers_count']
                following_count = status._json['user']['friends_count']
                overall_tweet_count = status._json['user']['statuses_count']
                favourite_count = status._json['favorite_count']
                retweet_count = status._json['retweet_count']
            tweet = {
                'Tweet_creation':created_at,
                'Tweet_id':tweet_id,
                'Tweet_text':tweet_text, 
                'Tweet_favourites':favourite_count, 
                'Tweet_retweets':retweet_count, 
                'Userhandle':userhandle, 
                'Username':username, 
                'User_location':location, 
                'Follower_count':follower_count, 
                'Following_count':following_count,
                'Overall_tweets': overall_tweet_count
                }  
            
            
            with open('yourFilename.json','a+', encoding='utf-8') as f:
                f.write(json.dumps(tweet))
                f.close()  
                
def Authenticate():
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    return tweepy.API(auth, parser=tweepy.parsers.JSONParser())
    
    
if __name__ == '__main__':

    myStreamListener = MyStreamListener()
    api = Authenticate()
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener, tweet_mode='extended', language='en', filter_level = 'medium')
    print(myStream.filter(track = ['football', 'hockey', 'baseball', 'soccer', 'basketball', 'tennis', 'volleyball', 'rugby']))


