import praw
from config import client_id, client_secret
import re

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent="review finder"
)
for submission in reddit.subreddit("learnpython").hot(limit=10):
    print(submission.title)
