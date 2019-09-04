"""
    News provider for the site elpais.com

    Checks specifically the Alzheimer tag
"""

from datetime import datetime
from textwrap import dedent
from lxml import html, etree
from lxml.cssselect import CSSSelector
import requests

URL = 'https://www.elmundo.es/ciencia-y-salud.html'
SITE = 'elmundo.es'


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

        link = CSSSelector('article .ue-c-cover-content__link')(article)[0].get('href')

        if "promo" in link.lower() or "follow" in link.lower():
            continue

        news_page = html.fromstring(requests.get(link).content)

        news_date = CSSSelector('time')(news_page)[0].get('datetime')
        news_datetime = datetime.strptime(news_date, '%Y-%m-%dT%H:%M:%SZ')

        if news_datetime < last_updated:
            break

        # Get the useful parts of each article to compose a tweet.
        title = CSSSelector('article .ue-c-cover-content__headline')(article)[0].text
        author = CSSSelector('.ue-c-article__byline-name a, .ue-c-article__byline-name')(news_page)[0].text
        article_body = str(etree.tostring(CSSSelector('.ue-l-article__body')(news_page)[0]))

        if "alzheimer" not in article_body.lower():
            continue

        # Compose a tweet with the article's information
        tweet = """
                {title}

                Autor/a: {author}
                Enlace: https:{link} ({site})
                """.format(title=title, author=author, link=link, site=SITE)

        to_ret.append(dedent(tweet))

    # Returns a list of tweets ready for the bot to tweet.
    return to_ret
