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
api = PushshiftAPI()

def get_from_reddit(item):

    results = {}
    reddit_posts = reddit.subreddit("all").search(
        item, 
        sort="best", 
        time_filter="month", 
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
                    title=item,
                    over_18="false",
                    limit=200
                    )
    print("bruh1")
    cur1 = 0
    cur2 = 0
    avgVotes = 0
    count = 0

    temp = []

    for item in gen:
        avgVotes += item.score
        count+=1
        temp.append((item.score,item.title))
    avgVotes = avgVotes/count
    print("average", avgVotes)
    
    for item in temp:
        #print(item.permalink)
        #print(item[1])
        sent = TextBlob(item[1]).sentiment
        #print(item[0]/avgVotes)
        if(sent.polarity > 0):
            cur1 += sent.polarity 
        else:
            cur2 += sent.polarity 
        
        #print(sent)
    return (cur1, cur2)


def get_graph_data(item):
    #results = [[0 for x in range(2)] for y in range(15)] 
    results = [1 for i in range(15)]
    start_epoch=int(dt.datetime(2020, 1, 1).timestamp())
    for i in range(1, 14):
        results[i] = (0, 0)
    for i in range(1, 14):
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
        
        results[i-1] = searchAPI(start_epoch, end_epoch, item)
        print("results: ", results[i-1][0], " ", results[i-1][1])
    
    





    return results


#for submission in reddit.subreddit("mechanicalkeyboards").hot(limit=10):
 #   testimonial = TextBlob(submission.title)
  #  print(submission.title)
   # print(testimonial.sentiment)

