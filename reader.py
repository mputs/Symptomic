### dependencies
import tweepy
import configparser as CFG
from os import path
from sys import exc_info
output = "out.csv"

def writeoutput(output, postfix, status, text):
    postfix = postfix.split(" ")[0].replace("/", "")
    filename = "output/"+output+postfix +".csv"
    print (filename)
    if not path.exists(filename):
        with open(filename, "w", encoding='utf-8') as f:
           f.write("date,user,text,location,geo,coordinates,place\n")

    with open(filename, "a", encoding='utf-8') as f:
                        f.write("'%s','%s','%s','%s','%s','%s','%s'\n" % ( \
                                status.created_at,\
                                status.user.screen_name,\
                                text,\
                                status.user.location,\
                                status.geo,\
                                status.coordinates,\
                                status.place \
                                ))

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
                
            writeoutput(output, status.created_at, status, text):
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

### initialize stream
streamListener = StreamListener()

try:
    ### authenticate
    stream = tweepy.Stream(auth=api.auth, listener=streamListener,tweet_mode='extended')
    ### listen
    stream.filter(track=tags)
except:
    print("error: ", exc_info()[0])

