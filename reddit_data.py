import praw
from config import client_id, client_secret
import re
from textblob import TextBlob
import datetime as dt
from psaw import PushshiftAPI
from datetime import datetime


reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent="review finder"
)
api = PushshiftAPI(max_results_per_request=100)

def get_from_reddit(item):

    results = {}
    reddit_posts = reddit.subreddit("all").search(
        item, 
        sort="best", 
        time_filter="year", 
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

#deprecated function that makes search queries for every time frame – migrated to one query and sorting to reduce query time
def searchAPI(start_epoch, end_epoch, item):
    gen =api.search_submissions(before=end_epoch,
                    after=start_epoch,
                    q = item,
                    sort = "asc",
                    sort_type = "score",
                    title=item,
                    over_18="false",
                    limit=50
                    )
    print("bruh1")
    cur1 = 0
    cur2 = 0
    avgVotes = 0
    count = 0

    temp = []

    for item in gen:
        count += 1
        avgVotes += item.score
        temp.append((item.score,item.title))
    
    for item in temp:
        #print(item.permalink)
        #print(item[1])
        sent = TextBlob(item[1]).sentiment
        #print(item[0]/avgVotes)
        if(sent.polarity > 0):
            cur1 += sent.polarity 
        else:
            cur2 += sent.polarity 

    return (cur1, cur2)

#retrieves reddit posts and determines polarity – returns an array with data for each month
def get_graph_data(item):
    #results = [[0 for x in range(2)] for y in range(15)] 
    start_epoch=int(dt.datetime(2020, 1, 1).timestamp())
    end_epoch=int(dt.datetime(2021, 2, 1).timestamp())

    gen =api.search_submissions(
                after=start_epoch,
                q = item,
                sort = "desc",
                sort_type = "score",
                title=item,
                over_18="false",
                limit=300
                )

    cur1 = 0
    cur2 = 0
    avgVotes = 0
    count = 0

    temp = [[] for i in range(15)]

    results = [(0, 0) for i in range(15)]
    c = 0
    lim = 2000

    for item in gen:
        #print(item.permalink)
        sent = TextBlob(item.title).sentiment.polarity

        ind = 0
        for i in range(1, 14):
            if i == 12:
                if int(dt.datetime(2020, 12, 1).timestamp()) < item.created_utc < int(dt.datetime(2021, 1, 1).timestamp()):
                    ind = i 
                    break
            elif i == 13:
                if int(dt.datetime(2021, 1, 1).timestamp()) < item.created_utc < int(dt.datetime(2021, 2, 1).timestamp()):
                    ind = i 
                    break
            else: 
                if int(dt.datetime(2020, i, 1).timestamp()) < item.created_utc < int(dt.datetime(2020, i+1, 1).timestamp()):
                    ind = i 
                    break

        temp[ind].append(sent)
        if ind == 4:
            print(item.permalink)
        c+=1
        if c > lim:
            break

    
    for i in range(1, 14):
        print(len(temp[i]))

    print(c)
    cnt = 0
    for i in range(1, 14):
        cur1 = 0
        cur2 = 0
        for item in temp[i]:
            cnt+=1
            if(item > 0):
                cur1 += item
            else:
                cur2 += item
        results[i-1] = (cur1, cur2)
    print(cnt)
        
    
#    for i in range(1, 14):
#        print(results[i-1])
    
    





    return results


#for submission in reddit.subreddit("mechanicalkeyboards").hot(limit=10):
 #   testimonial = TextBlob(submission.title)
  #  print(submission.title)
   # print(testimonial.sentiment)

