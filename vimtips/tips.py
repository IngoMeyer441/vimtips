import json
import os
import random
import threading
import time
from typing import cast, Any, Callable, Dict, List, NamedTuple, Optional  # noqa: F401  # pylint: disable=unused-import
from . import sources

DEFAULT_CACHE_LOCATION = os.path.expanduser('~/.vimtips_cache')

TipWithTimestamp = NamedTuple('TipWithTimestamp', [('tip', str), ('timestamp', float)])


class TipHistory:
    class NoPreviousTipError(Exception):
        pass

    def __init__(self) -> None:
        self._history = []  # type: List[TipWithTimestamp]
        self._history_index = 0

    def next_random_tip(self) -> TipWithTimestamp:
        _tip_cache = tip_cache_box.tip_cache  # Read the variable only once to prevent threading problems
        tip_with_timestamp = TipWithTimestamp(_tip_cache.random_tip, _tip_cache.timestamp)
        self._history.append(tip_with_timestamp)
        self._history_index = len(self._history)
        return tip_with_timestamp

    def previous_tip(self) -> TipWithTimestamp:
        if self.has_previous_tip:
            self._history_index -= 1
            return self._history[self._history_index - 1]
        else:
            raise self.NoPreviousTipError

    def next_tip(self) -> TipWithTimestamp:
        if self._history_index == len(self._history):
            return self.next_random_tip()
        else:
            self._history_index += 1
            return self._history[self._history_index - 1]

    @property
    def history(self) -> List[TipWithTimestamp]:
        return self._history

    @property
    def history_index(self) -> int:
        return self._history_index

    @property
    def has_previous_tip(self) -> bool:
        return self._history_index > 1

    def __len__(self) -> int:
        return len(self._history)


class TipCache:
    class CacheReadError(Exception):
        pass

    class CacheCorruptedError(Exception):
        pass

    class CacheWriteError(Exception):
        pass

    def __init__(self, cache_location: str = DEFAULT_CACHE_LOCATION) -> None:
        self._cache_location = cache_location
        self._timestamp = None  # type: Optional[float]
        self._tips = None  # type: Optional[List[str]]

    def _init_cache_data(self) -> None:
        try:
            self._read_cache()
        except (self.CacheReadError, self.CacheCorruptedError):
            self.renew_cache()

    def _read_cache(self) -> None:
        try:
            with open(self._cache_location, 'r') as f:
                cache_file_content = json.load(f)  # type: Dict[str, Any]
        except (IOError, json.JSONDecodeError):
            raise self.CacheReadError('Could not load cache file {}'.format(self._cache_location))
        try:
            cache_timestamp = float(cache_file_content['timestamp'])
            cache_content = [str(tip) for tip in cache_file_content['tips']]
        except (KeyError, ValueError):
            raise self.CacheCorruptedError('The cache file {} is corrupted.'.format(self._cache_location))
        self._timestamp = cache_timestamp
        self._tips = cache_content

    def _write_cache(self) -> None:
        cache_content = {'timestamp': self._timestamp, 'tips': self._tips}
        try:
            with open(self._cache_location, 'w') as f:
                json.dump(cache_content, f)
        except IOError:
            raise self.CacheWriteError('Could not write cache file {}'.format(self._cache_location))

    def renew_cache(self) -> None:
        self._tips = sources.load_all_tips()
        self._timestamp = time.time()
        self._write_cache()

    @property
    def timestamp(self) -> float:
        if self._timestamp is None:
            self._init_cache_data()
        return cast(float, self._timestamp)

    @property
    def tips(self) -> List[str]:
        if self._tips is None:
            self._init_cache_data()
        return cast(List[str], self._tips)

    @property
    def random_tip(self) -> str:
        random_tip = self.tips[random.randrange(len(self.tips))]
        return random_tip


# Use a wrapper class to update the cache object asynchronously safely -> create new cache object and replace the old
# one in the box.
class TipCacheBox:
    def __init__(self) -> None:
        self._tip_cache = TipCache()

    def update_asynchronously(self, thread_type: Callable = threading.Thread) -> Any:
        def job_function() -> None:
            tip_cache = TipCache()
            tip_cache.renew_cache()
            self._tip_cache = tip_cache

        thread = thread_type(target=job_function)
        thread.start()
        return thread

    @property
    def tip_cache(self) -> TipCache:
        return self._tip_cache


tip_cache_box = TipCacheBox()
