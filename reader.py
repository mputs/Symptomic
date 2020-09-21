### dependencies
import tweepy
import configparser as CFG
from os import path

output = "out.csv"

### StreamListener 
#   Remove retweets and quotes
#   
class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        # if "retweeted_status" attribute exists, flag this tweet as a retweet.
        is_retweet = hasattr(status, "retweeted_status")
        # check if this is a quote tweet.
        is_quote = hasattr(status, "quoted_status")
        if (not is_quote) & (not is_retweet):
            # check if text has been truncated
            if hasattr(status,"extended_tweet"):
                text = status.extended_tweet["full_text"]
            else:
                text = status.text

        
            # remove characters that might cause problems with csv encoding
            remove_characters = [",","\n"]
            for c in remove_characters:
                text = text.replace(c," ")
            with open("output/"+output, "a", encoding='utf-8') as f:
                                f.write("%s,%s,%s,%s,%s,%s,%s\n" % ( \
                                        status.created_at,\
                                        status.user.screen_name,\
                                        text,\
                                        status.user.location,\
                                        status.geo,\
                                        status.coordinates,\
                                        status.place \
                                       ))
  
    def on_error(self, status_code):
        print("Encountered streaming error (", status_code, ")")
        sys.exit()

### read configuration
cfg = CFG.ConfigParser()
cfg.read("settings.cfg")

# Tags are written in multiline. Use indents for that
tags = [c for c in cfg['track']['tags'].split("\n") if c != ""]
# these are the credentials for the twitter api.
consumer_key = cfg["credentials"]["consumer_key"]
consumer_secret = cfg["credentials"]["consumer_secret"]
access_key = cfg["credentials"]["access_key"]
access_secret = cfg["credentials"]["access_secret"]
# specify the name of the output file.
output = cfg['output']['filename']

### Connect to twitter.
# set credentials
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
# initialize api
api = tweepy.API(auth)

### set output
if not path.exists("output/"+output):
    with open("output/"+output, "w", encoding='utf-8') as f:
        f.write("date,user,text,location,geo,coordinates,place\n")


### initialize stream
streamListener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=streamListener,tweet_mode='extended')

### listen
stream.filter(track=tags)

