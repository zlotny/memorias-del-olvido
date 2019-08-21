"""
    This application provides a Twitter bot that polls different providers for news on the net.

    Each provider then returns tweets with news from a date on, to be tweeted by the bot.

    See LICENSE file for the license information
"""

from os import getenv
from os.path import join, dirname
from time import sleep
from datetime import datetime

import tweepy
from tweepy.error import TweepError
from dotenv import load_dotenv

from news_providers import example

ENV_FILE = '.env'
DEFAULT_CHECK_DELAY = 3600
NEWS_PROVIDERS = [example]

load_dotenv(join(dirname(__file__), ENV_FILE))


def main():
    """ Main function of the application. Creates a twitter bot that tweets every now and then. """

    # Twitter authentication
    auth = tweepy.OAuthHandler(getenv('CONSUMER_KEY'), getenv('CONSUMER_SECRET'))
    auth.set_access_token(getenv('ACCESS_TOKEN'), getenv('ACCESS_TOKEN_SECRET'))

    api = tweepy.API(auth)

    # Bot configuration
    check_delay = int(getenv('CHECK_DELAY') or DEFAULT_CHECK_DELAY)

    # Check that authentication was correct
    try:
        api.me().screen_name
    except TweepError:
        print('''Couldn't perform authentication. Check your twitter keys and secrets.''')
        return

    print('Logged in as {}!'.format(api.me().screen_name))

    # Setup check-tweets iteration
    last_checked = datetime.now()
    to_tweet = list()
    tweet_counter = 0

    while True:
        # Retrieve tweets from providers
        for provider in NEWS_PROVIDERS:
            to_tweet.extend(provider.retrieve(last_checked))

        # Process tweets
        for tweet in to_tweet:
            try:
                api.update_status(tweet)
                tweet_counter += 1
            except TweepError as error:
                print('Found an error tweeting. Error message was: {}'.format(error.response.text))
        print('Managed to tweet {} tweets out of the retrieved {} on this iteration'.format(tweet_counter, len(to_tweet)))

        # Clean and update results for the next iteration
        tweet_counter = 0
        last_checked = datetime.now()
        to_tweet = list()

        # Wait a bit
        sleep(check_delay)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Exiting bot execution.')
