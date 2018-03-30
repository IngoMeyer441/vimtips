import json
import os
import random
import time
from typing import cast, Any, Dict, Iterator, List, NamedTuple, Optional, Tuple
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
        try:
            tip_with_timestamp = random_cached_tip()
        except Cache.ReadError:
            renew_cache()
            tip_with_timestamp = random_cached_tip()
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


class Cache:
    class ReadError(Exception):
        pass

    class CorruptedError(Exception):
        pass

    class WriteError(Exception):
        pass

    def __init__(self, cache_location: str=DEFAULT_CACHE_LOCATION) -> None:
        self._cache_location = cache_location
        self._timestamp = None  # type: Optional[float]
        self._tips = None  # type: Optional[List[str]]

    def _read_cache(self) -> None:
        try:
            with open(self._cache_location, 'r') as f:
                cache_file_content = json.load(f)  # type: Dict[str, Any]
        except (IOError, json.JSONDecodeError):
            raise self.ReadError('Could not load cache file {}'.format(self._cache_location))
        try:
            cache_timestamp = float(cache_file_content['timestamp'])
            cache_content = [str(tip) for tip in cache_file_content['tips']]
        except (KeyError, ValueError):
            raise self.CorruptedError('The cache file {} is corrupted.'.format(self._cache_location))
        self._timestamp = cache_timestamp
        self._tips = cache_content

    def _write_cache(self) -> None:
        cache_content = {
            'timestamp': self._timestamp,
            'tips': self._tips
        }
        try:
            with open(self._cache_location, 'w') as f:
                json.dump(cache_content, f)
        except IOError:
            raise self.WriteError('Could not write cache file {}'.format(self._cache_location))

    @property
    def timestamp(self) -> float:
        if self._timestamp is None:
            self._read_cache()
        return cast(float, self._timestamp)

    @property
    def tips(self) -> List[str]:
        if self._tips is None:
            self._read_cache()
        return cast(List[str], self._tips)

    @tips.setter
    def tips(self, value: Iterator[str]) -> None:
        self._tips = list(value)
        self._timestamp = time.time()
        self._write_cache()


_cache = Cache()


def cached_tips() -> Tuple[List[str], float]:
    return _cache.tips, _cache.timestamp


def random_cached_tip() -> TipWithTimestamp:
    tips = _cache.tips
    random_tip = tips[random.randrange(len(tips))]
    return TipWithTimestamp(random_tip, _cache.timestamp)


def renew_cache() -> None:
    _cache.tips = sources.load_all_tips()
