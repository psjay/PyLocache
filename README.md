# PyLocache

[![Build Status](https://travis-ci.org/psjay/PyLocache.svg?branch=master)](https://travis-ci.org/psjay/PyLocache)

PyLocache is a Python implementation of LRU local cache.

## Usage

```python
cache = LocalCache(max_size=5)
cache.set('foo', 1)
cache.set('bar', 2)

cache.get('foo')  # 1

cache.set('hello', 'world', expires=3)  # expires in 3 seconds.

# All items of it will be expired in 2 seconds after being set.
volatile_cache = LocalCache(max_size=5, expires=2)
```
