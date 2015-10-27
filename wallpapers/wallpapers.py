import requests
import praw
import os


here = os.path.dirname(os.path.abspath(__file__)) 


def download(url):
    response = requests.get(url)
    return response.content


def save(filename, wallpaper):
    with open(filename, 'w') as f:
        f.write(wallpaper)


reddit = praw.Reddit(user_agent='earthporn_wallpapers_downloader')
submissions = reddit.get_subreddit('earthporn').get_top_from_week()

for submission in submissions:
    if 'imgur' in submission.url:
        if submission.url.endswith('jpg'):
            print "Downloading: %s" % submission.title
            wallpaper = download(submission.url)
            print "Saving as: %s" % submission.url.split('/')[-1]
            save(here + '/' + submission.url.split('/')[-1], wallpaper)

print "Done"

