"""
    A news provider example for the twitter bot.
    A module based on this MUST include the retrieve function with the same signature.

    See LICENSE file for the license information
"""

from datetime import datetime


def retrieve(last_updated=datetime.now()):
    """ Simulates news crawling and returns a list of sample tweets to test the application. """
    print('Retrieving sample news since {}.'.format(last_updated))
    return ['first_tweet', 'second_tweet']
