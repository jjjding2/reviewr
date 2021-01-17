import praw
from config import client_id, client_secret
import re
from textblob import TextBlob
import datetime as dt
from psaw import PushshiftAPI


reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent="review finder"
)
api = PushshiftAPI(reddit)

def get_from_reddit(item):

    results = {}
    reddit_posts = reddit.subreddit("all").search(
        item, 
        sort="best", 
        time_filter="week", 
        limit = 10,
    )

    for item in reddit_posts:
        #print(item.title)

        results[item.title] = {
            "text": item.selftext,
            "url": "https://www.reddit.com" + item.permalink,
        }
        #print(item.permalink)
    return results

def searchAPI(start_epoch, end_epoch, item):
    gen =api.search_submissions(before=end_epoch,
                    after=start_epoch,
                    q = item,
                    sort = "desc",
                    sort_type = "score",
                    limit=15,
                    title=item,
                    over_18="false"
                    )
    print("bruh1")
    cur = 0
    for item in gen:
        print(item.permalink)
        sent = TextBlob(item.title).sentiment
        cur+=sent.polarity
        print(sent)
    return cur


def get_graph_data(item):
    results = [[0 for x in range(2)] for y in range(15)] 
    start_epoch=int(dt.datetime(2020, 1, 1).timestamp())
    for i in range(1, 13):
        results[i][0] = 0
    for i in range(9, 14):
        api = PushshiftAPI(reddit)
        print(i)

        if i == 12:
            start_epoch=int(dt.datetime(2020, i, 1).timestamp())
            end_epoch=int(dt.datetime(2021, 1, 1).timestamp())
        elif i == 13:
            start_epoch=int(dt.datetime(2021, 1, 1).timestamp())
            end_epoch=int(dt.datetime(2021, 2, 1).timestamp())
        else:
            start_epoch=int(dt.datetime(2020, i, 1).timestamp())
            end_epoch=int(dt.datetime(2020, i+1, 1).timestamp())
        
        results[i][0] = searchAPI(start_epoch, end_epoch, item)
        print("results: ", results[i][0])
        





    return results


#for submission in reddit.subreddit("mechanicalkeyboards").hot(limit=10):
 #   testimonial = TextBlob(submission.title)
  #  print(submission.title)
   # print(testimonial.sentiment)

