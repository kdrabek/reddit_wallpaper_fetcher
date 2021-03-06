import logging

from praw import Reddit
import requests


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('wallpapers_fetcher')


def prepare_filename(url):
    return url.split('/')[-1]


def prepare_image_download_url(url):
    if 'imgur' in url or 'staticflickr' in url:
        if url.endswith('.jpg'):
            return url
        else:
            return '{}.jpg'.format(url)
    return None


def download(url):
    try:
        response = requests.get(url, stream=True)
    except requests.exceptions.RequestException as e:
        log.error(
            'Error occurred when downloading {0}, message: {1}'.format(
                url, e.message)
        )
        raise
    else:
        log.info('Downloaded: {0}'.format(url))
        return response.raw


def get_reddit_submissions(subreddit='earthporn'):
    reddit = Reddit(user_agent='earthporn_wallpapers_downloader')
    submissions = reddit.get_subreddit(subreddit).get_top_from_week()
    log.info('Fetching submissions from "{0}"'.format(subreddit))
    return submissions


def proper_dimensions(width, height, image, scale_coefficient=0.9):
    image_width, image_height = image.size
    return (width * scale_coefficient <= image_width and
            height * scale_coefficient <= image_height)
