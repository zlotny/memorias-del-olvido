"""
    News provider for the site rtve.es

    Checks specifically the Alzheimer tag. Only checks news, not videos or audios
"""

from datetime import datetime
from textwrap import dedent
from lxml import html
from lxml.cssselect import CSSSelector
import requests

URL = 'http://www.rtve.es/temas/alzheimer/1060/'
SITE = 'rtve.es'


def retrieve(last_updated=datetime.now()):
    """ Crawls news and returns a list of tweets to publish. """
    print('Retrieving {} alzheimer news since {}.'.format(SITE, last_updated))

    to_ret = list()

    # Get all the content from the last page of the site's news
    tree = html.fromstring(requests.get(URL).content)

    # Get list of articles
    articles = CSSSelector('article')(tree)

    for article in articles:
        # For each article parse the date on the metadata and compare to the last update of the bot.
        # If the article is newer it should go on until it finds one that's not

        link = CSSSelector('article h2 a')(article)[0].get('href')
        
        if "/noticias/" not in link.lower():
            continue


        news_date = CSSSelector('article time')(article)[0].get('datetime')
        news_datetime = datetime.strptime(news_date, '%Y-%m-%d')


        if news_datetime < last_updated:
            break

        # Get the useful parts of each article to compose a tweet.
        title_raw = CSSSelector('article .maintitle')(article)[0].text

        title = ' '.join(title_raw.split())

        # Compose a tweet with the article's information
        tweet = """
                {title}

                Autor/a: RTVE.es
                Enlace: {link} ({site})
                """.format(title=title, link=link, site=SITE)

        to_ret.append(dedent(tweet))

    # Returns a list of tweets ready for the bot to tweet.
    return to_ret
