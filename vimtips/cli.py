#!/usr/bin/env python3

import sys
from datetime import datetime
from .tips import tip_cache_box


def print_random_tip() -> None:
    tip_cache = tip_cache_box.tip_cache
    random_cached_tip, timestamp = tip_cache.random_tip, tip_cache.timestamp
    print("cache timestamp: {}".format(datetime.fromtimestamp(timestamp).ctime()), file=sys.stderr)
    print(random_cached_tip)


def main() -> None:
    print_random_tip()


if __name__ == "__main__":
    main()
