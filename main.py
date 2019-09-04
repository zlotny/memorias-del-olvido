"""
    This application provides a Twitter bot that polls different providers for news on the net.

    Each provider then returns tweets with news from a date on, to be tweeted by the bot.

    See LICENSE file for the license information
"""

from os import getenv
from os.path import join, dirname
from time import sleep
from datetime import datetime, timedelta
import traceback

import tweepy
from tweepy.error import TweepError
from dotenv import load_dotenv

from news_providers import elpais, elmundo, abc, rtve

# Environment loading
ENV_FILE = '.env'
load_dotenv(join(dirname(__file__), ENV_FILE))

# Environment configuration
DEFAULT_CHECK_DELAY = 3600
NEWS_PROVIDERS = [elpais, elmundo, abc, rtve]
DEBUG_MODE = getenv('DEBUG_MODE').lower() == "true" or False
DELETE_ALL_AT_START = getenv('DELETE_ALL_AT_START').lower() == "true" or False


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

    if DEBUG_MODE:
        print('Logged in as {}!'.format(api.me().screen_name))

    if DELETE_ALL_AT_START:
        for status in tweepy.Cursor(api.user_timeline).items():
            try:
                api.destroy_status(status.id)
            except:
                print("Failed to delete: {}".format(status.id))

    # Setup check-tweets iteration
    last_checked = datetime.now()

    if DEBUG_MODE:
        last_checked -= timedelta(days=10)

    to_tweet = list()
    tweet_counter = 0

    while True:
        # Retrieve tweets from providers
        for provider in NEWS_PROVIDERS:
            new_tweets = list()

            try:
                new_tweets = provider.retrieve(last_checked)
            except IndexError:
                print("There was an error retrieving the last tweets. Ignoring the site: {}".format(provider.SITE))
                if DEBUG_MODE:
                    traceback.print_exc()

            to_tweet.extend(new_tweets)

        # Process tweets
        for tweet in to_tweet:
            try:
                if DEBUG_MODE:
                    print("""
                        Tweet:
                        {}


                    """.format(tweet))
                else:
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
