import logging
import os

import click
from PIL import Image

from utils import (
    get_reddit_submissions, prepare_image_download_url, download, 
    proper_dimensions, prepare_filename)


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('wallpapers_fetcher')


@click.command()
@click.option('--height', default=1080, help='Minimum height of the image.')
@click.option('--width', default=1920, help='Minimum widht of the image.')
@click.option(
    '--subreddit', default='earthporn', help='Subreddit to fetch images from')
def download_wallpapers(subreddit, width, height):
    import time
    start = time.time()
    submissions = get_reddit_submissions(subreddit)
    for submission in submissions:
        image_url = prepare_image_download_url(submission.url)
        if image_url:
            wallpaper = download(image_url)
            img = Image.open(wallpaper)
            if proper_dimensions(width, height, img):
                img.save(
                        os.path.join(os.getcwd(), '../downloads', 
                        prepare_filename(image_url)), "JPEG"
                    )
            else:
                log.info("Skipping {}, reason: too small".format(image_url))
        else:
            log.info("Skipping {0}".format(submission.url))
    log.info("It took %s seconds to download and save the files" % (
        time.time() - start))

if __name__ == '__main__':
    download_wallpapers()
