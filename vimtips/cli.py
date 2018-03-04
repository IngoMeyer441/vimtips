#!/usr/bin/env python3

import sys
from datetime import datetime
from . import tips


def print_random_tip() -> None:
    try:
        random_cached_tip, timestamp = tips.random_cached_tip()
        print('Using cache, timestamp: {}'.format(datetime.fromtimestamp(timestamp).ctime()), file=sys.stderr)
    except tips.Cache.ReadError:
        print('No cache found -> refreshing', file=sys.stderr)
        tips.renew_cache()
        random_cached_tip, timestamp = tips.random_cached_tip()
    print(random_cached_tip)


def main() -> None:
    print_random_tip()


if __name__ == '__main__':
    main()
