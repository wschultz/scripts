#!/usr/bin/env python
 
import os
import twitter
import time

# Create an Api instance.
api = twitter.Api(consumer_key=os.environ.get('CONSUMER_KEY'),
                  consumer_secret=os.environ.get('CONSUMER_SECRET'),
                  access_token_key=os.environ.get('ACCESS_TOKEN'),
                  access_token_secret=os.environ.get('ACCESS_TOKEN_SECRET'))

# Change these variables here
days_ago         = 3           # How many days do we keep?
screen_name      = "vileTexan" # What's your twitter handle?
delete_tweets    = True        # True/False... If True, delete Tweets
delete_favorites = True        # True/False... If True, delete Favorites
delete_lists     = True        # True/False... If True, delete Lists people have put you on

# What are the Tweet IDs you don't want to delete?
safe_ids = [
  1638218044877971470,
  1653730123865104384,
  1653225476335255552,
  1651954469511352320,
  1653512857214959619, # Mercy's list
]

cutoff = int(time.time()) - (days_ago * 24 * 60 * 60)
max_id = 0

def DeleteTweets(cutoff):
  tweets = api.GetUserTimeline(screen_name=screen_name, count=200, include_rts=True) 

  try:
    while len(tweets) > 1:
      for tweet in tweets:
        if tweet.created_at_in_seconds < cutoff and tweet.id not in safe_ids:
          print("Deleting tweet: ", tweet.id, tweet.created_at, tweet.text)
          api.DestroyStatus(status_id=tweet.id)

      max_id = tweet.id

      tweets = api.GetUserTimeline(screen_name=screen_name, count=200, include_rts=True, max_id=max_id)

      if len(tweets) == 1:
        api.DestroyStatus(status_id=tweet.id)
        break

  except Exception as err:
    print(err.message)
    for i in err.message:
      print(i)


def DeleteFavorites(cutoff):
  favs = api.GetFavorites(screen_name=screen_name, count=200)

  try:
    while len(favs) > 1:
      for fav in favs:
        if fav.created_at_in_seconds < cutoff:
          print("Deleting Fav: ", fav.id, fav.created_at, fav.text)
          api.DestroyFavorite(status_id=fav.id)

      max_id = fav.id

      favs = api.GetFavorites(screen_name=screen_name, count=200, max_id=max_id)

      if len(favs) == 1:
        api.DestroyFavorite(status_id=fav.id)
        break

  except Exception as err:
    print(err.message)
    for i in err.message:
      print(i)

def DeleteLists():
  lists = api.GetMemberships(screen_name=screen_name, count=1000)

  try:
    for i in lists:
      if i.id not in safe_ids:
        print("Deleting List: " + i.id)
        api.CreateBlock(user_id=i.user.id)
        time.sleep(1)
        api.DestroyBlock(user_id=i.user.id)

  except Exception as err:
    print(err.message)
    for i in err.message:
      print(i)

if __name__ == "__main__":
  if delete_tweets == True:
    DeleteTweets(cutoff)
  if delete_favorites == True:
    DeleteFavorites(cutoff)
  if delete_lists == True:
    DeleteLists()

