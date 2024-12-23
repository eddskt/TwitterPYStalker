import tweepy
from twilio.rest import Client
import time
from envDEV import *

#Twitter Auth
auth = tweepy.OAuth1UserHandler(
  TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET
)
twitter_api = tweepy.API(auth)

#Twilio Auth
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

#Function to search last tts
def get_lastest_tweets(username, since_id=None):
  tweets = twitter_api.user_timeline(screen_name=username, since_id=since_id, tweet_mode="extended")
  return tweets

#Function to search replies
def get_replies_to_tweet(tweet_id, username):
  query = f"to:{username}"
  replies = twitter_api.search_tweets(q=query, since_id=tweet_id, tweet_mode="extended")
  return replies

#Function to send a whatsapp message
def send_whatsapp_message(message):
  twilio_client.messages.create(
    from_=TWILIO_WHATSAPP_NUMBER,
    body=message,
    to=USER_WHATSAPP_NUMBER
  )

#Function to monitor and send alerts
def monitor_tweets():
  last_seen_id = None

  while True:
    tweets = get_lastest_tweets(TWITTER_USERNAME, since_id=last_seen_id)

    for tweet in reversed(tweets):
      tweet_text = f"Novo Tweet de {TWITTER_USERNAME}: {tweet.full_text}"
      send_whatsapp_message(tweet_text)
      print(tweet_text)

      #Replies Monitor
      replies = get_replies_to_tweet(tweet.id, TWITTER_USERNAME)
      for reply in replies:
        print(reply)
        reply_text = f"Resposta ao Tweet {tweet.id}: {reply.full_text}"
        send_whatsapp_message(reply_text)
        print(reply_text)

      last_seen_id = tweet.id

    time.sleep(60)

#Starts Monitoring
if __name__ == "__main__":
  monitor_tweets()

