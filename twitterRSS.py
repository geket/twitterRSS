import os
import tweepy
import discord
from discord import Webhook, RequestsWebhookAdapter
import asyncio

consumer_key = "your_consumer_key_here"
consumer_secret = "your_consumer_secret_here"
access_token = "your_access_token_here"
access_token_secret = "your_access_token_secret_here"

auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)

api = tweepy.API(auth)

webhook_url = "your_webhook_url_here"
webhook = Webhook.from_url(webhook_url, adapter=RequestsWebhookAdapter())

def get_latest_tweets():
    tweets = api.user_timeline(
        screen_name="twitter_username_here",
        count=10,
        include_rts=False,
        tweet_mode="extended",
    )
    return tweets

def format_tweet(tweet):
    message = f"**{tweet.user.name} (@{tweet.user.screen_name}):**\n{tweet.full_text}"
    if tweet.entities.get("urls"):
        message += "\n" + " ".join(url["url"] for url in tweet.entities["urls"])
    return message

async def check_tweets():
    latest_tweets = set()
    while True:
        tweets = get_latest_tweets()
        for tweet in tweets:
            if tweet.id not in latest_tweets:
                message = format_tweet(tweet)
                webhook.send(message)
                latest_tweets.add(tweet.id)
        await asyncio.sleep(300) # Check every 5 minutes

check_tweets_task = asyncio.ensure_future(check_tweets())
