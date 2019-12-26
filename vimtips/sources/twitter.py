import requests
import time
from pyquery import PyQuery
from typing import List


VIMTIPS_ACCOUNTS = ["vimtips", "VImTipsDaily", "vimpal", "VimTip"]
MAX_TRIES = 5
WAIT_TIME_BETWEEN_TRIES = 10  # seconds


class TweetQueryError(Exception):
    pass


def load_tweets(username: str) -> List[str]:
    cursor = ""
    tweets = []  # type: List[str]
    while True:
        for _ in range(MAX_TRIES):
            response = requests.get(
                "https://twitter.com/i/search/timeline?q=from%3A{}&max_position={}".format(username, cursor),
                headers={"user-agent": "Chrome/65.0", "accept": "application/json"},
            )
            if response.status_code == 200:
                try:
                    response_json = response.json()
                    break
                except ValueError:
                    pass
            time.sleep(WAIT_TIME_BETWEEN_TRIES)
        else:
            raise TweetQueryError
        cursor = response_json["min_position"]
        has_more_items = response_json["items_html"].strip() != ""
        if not has_more_items:
            break
        response_pq = PyQuery(response_json["items_html"])
        tweets_pq = [elem for elem in response_pq.items(".js-tweet-text-container")]
        tweets.extend([tweet_pq.text().replace("\n", " ") for tweet_pq in tweets_pq])
    return tweets


def tips() -> List[str]:
    tweets = []  # type: List[str]
    for account in VIMTIPS_ACCOUNTS:
        tweets.extend(load_tweets(account))
    return tweets
