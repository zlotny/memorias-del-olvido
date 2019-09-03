"""
    News provider for the site elpais.com

    Checks specifically the Alzheimer tag
"""

from datetime import datetime
from textwrap import dedent
from lxml import html
from lxml.cssselect import CSSSelector
import requests

URL = 'https://elpais.com/tag/alzheimer'
SITE = 'elpais.com'


def retrieve(last_updated=datetime.now()):
    """ Crawls news and returns a list of tweets to publish. """
    print('Retrieving {} alzheimer news since {}.'.format(SITE, last_updated))

    to_ret = list()

    # Get all the content from the last page of the site's news
    page = requests.get(URL)
    tree = html.fromstring(page.content)

    # Get list of articles
    articles = CSSSelector('article.articulo')(tree)

    for article in articles:
        # For each article parse the date on the metadata and compare to the last update of the bot.
        # If the article is newer it should go on until it finds one that's not

        news_date = CSSSelector('article.articulo .articulo-metadatos time')(article)[0].get('datetime')
        news_datetime = datetime.strptime(news_date, '%Y-%m-%dT%H:%M:%S')

        if news_datetime < last_updated:
            break

        # Get the useful parts of each article to compose a tweet.
        header = CSSSelector('article.articulo .articulo-titulo a')(article)[0]
        body = CSSSelector('article.articulo .articulo-entradilla')(article)[0].text
        author = CSSSelector('article.articulo .articulo-metadatos .autor-nombre a')(article)[0].text
        title = header.text
        link = header.get('href')

        # Compose a tweet with the article's information
        tweet = """
                {title}

                Autor/a: {author}
                Enlace: https:{link} ({site})
                """.format(title=title, author=author, link=link, site=SITE)

        to_ret.append(dedent(tweet))

    # Returns a list of tweets ready for the bot to tweet.
    return to_ret
