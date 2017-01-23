#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import time
import unittest

from nose.tools import eq_

from pylocache import LocalCache


class LocalCacheTest(unittest.TestCase):

    def base_test(self):
        cache = LocalCache(5)
        cache.set('foo', 1)
        cache.set('bar', 2)
        eq_(cache.get('foo'), 1)
        eq_(cache.get('bar'), 2)
        eq_(dict(cache), {
            'bar': 2,
            'foo': 1,
        })
        cache.set('hello', 'world')
        eq_(dict(cache), {
            'hello': 'world',
            'bar': 2,
            'foo': 1,
        })
        cache.delete('bar')
        cache.delete('something')
        eq_(dict(cache), {
            'hello': 'world',
            'foo': 1,
        })

    def lru_test(self):
        cache = LocalCache(5)
        cache.set('1', 1)
        cache.set('2', 2)
        cache.set('3', 3)
        cache.get('1')
        eq_(list(cache), [
            ('1', 1),
            ('3', 3),
            ('2', 2),
        ])
        cache.set('2', 4)
        eq_(list(cache), [
            ('2', 4),
            ('1', 1),
            ('3', 3),
        ])
        eq_(len(list(cache)), 3)

    def max_size_test(self):
        cache = LocalCache(3)
        cache.set('1', 1)
        cache.set('2', 2)
        eq_(len(list(cache)), 2)
        cache.set('3', 3)
        eq_(len(list(cache)), 3)
        cache.set('4', 4)
        eq_(len(list(cache)), 3)
        eq_(list(cache), [
            ('4', 4),
            ('3', 3),
            ('2', 2),
        ])

    def expires_test(self):
        cache = LocalCache(3, expires=1)
        cache.set('1', 1)
        cache.set('2', 2, expires=5)
        eq_(cache.get('1'), 1)
        eq_(cache.get('2'), 2)
        eq_(len(list(cache)), 2)
        time.sleep(2)
        eq_(cache.get('1'), None)
        eq_(cache.get('2'), 2)
        eq_(len(list(cache)), 1)

    def thread_safe_test(self):
        total = 100000
        batch_size = 10000
        cache = LocalCache(total * 2)
        threads = []
        for i in range(0, total, int(batch_size / 2)):
            thread = threading.Thread(target=self.__cache_numbers,
                                      args=(cache, range(i, i + batch_size if i + batch_size <= total else total))
                                      )
            threads.append(thread)
        [t.start() for t in threads]
        [t.join() for t in threads]

        eq_(len(list(cache)), total)

    def __cache_numbers(self, cache, nums):
        for n in nums:
            cache.set(str(n), n)

    def iterm_test(self):
        cache = LocalCache(3)
        cache.set('1', 1)
        cache.set('2', 2, expires=2)
        cache.set('3', 3)
        time.sleep(3)
        cached = set()
        for key, value in cache:
            cache.get(key)
            cached.add((key, value))

        assert cached == set([('1', 1), ('3', 3)])

    def test_get_default(self):
        cache = LocalCache(3)
        assert cache.get('1', 1) == 1
        assert cache.get('1', 2) == 2
        assert not list(cache)
