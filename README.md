# tumblr-backup-tool

This is a script made in python to back up videos, images (including .gifs) and photosets in your TUMBLR likes page (https://www.tumblr.com/likes)

Use the following libraries to use this script (other libraries used should be default within python):

import bs4
import requests
import urllib
import tqdm

KNOWN ISSUES

1.If a video doesn't exist anymore, the downloader will throw an error and exit the whole download queue instead of continuing

2.If the download queue is very long, probability is at some point it will throw an access denied error

3.I haven't implemented the ability to decide where videos are saved to, so right now everything points to C:\\Users\\asus\\.spyder-py3\\my scripts\\data\ for videos and C:\\Users\\asus\\.spyder-py3\\my scripts\\data\\pics for pics

This is my first script! Any comments or suggestions or help very welcome!
