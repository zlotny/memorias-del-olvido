"""
    News provider for the site abc.es

    Checks specifically the Alzheimer tag
"""

from datetime import datetime
from textwrap import dedent
from lxml import html
from lxml.cssselect import CSSSelector
import requests

URL = 'https://www.abc.es/salud/enfermedades/alzheimer/'
SITE = 'abc.es'


def retrieve(last_updated=datetime.now()):
    """ Crawls news and returns a list of tweets to publish. """
    print('Retrieving {} alzheimer news since {}.'.format(SITE, last_updated))

    to_ret = list()

    # Get all the content from the last page of the site's news
    tree = html.fromstring(requests.get(URL).content)

    # Get list of articles
    articles = CSSSelector('article:not(.destacado)')(tree)

    for article in articles:
        # For each article parse the date on the metadata and compare to the last update of the bot.
        # If the article is newer it should go on until it finds one that's not

        link = CSSSelector('article .titular a')(article)[0].get('href')

        news_date = CSSSelector('article time')(article)[0].get('datetime').split("+")[0]
        news_datetime = datetime.strptime(news_date, '%d/%m/%YT%H:%M:%S')

        if news_datetime < last_updated:
            break

        # Get the useful parts of each article to compose a tweet.
        title_raw = CSSSelector('article .titular a')(article)[0].text
        author_raw = CSSSelector('article .firma')(article)[0].text

        title = ' '.join(title_raw.split())
        author = ' '.join(author_raw.split())

        # Compose a tweet with the article's information
        tweet = """
                {title}

                Autor/a: {author}
                Enlace: {link} ({site})
                """.format(title=title, author=author, link=link, site=SITE)

        to_ret.append(dedent(tweet))

    # Returns a list of tweets ready for the bot to tweet.
    return to_ret
