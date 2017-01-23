#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import time


class LocalCache(object):

    def __init__(self, max_size=10000, expires=None):
        self._max_size = max_size
        self._cache_content = {}
        self._head = None
        self._tail = None
        self._expires = expires
        self._lock = threading.RLock()

    def get(self, k, default=None):
        with self._lock:
            e = self._cache_content.get(k, None)

            if e:
                if e.expired:
                    self._cache_content.pop(e.key)
                    self._remove(e)
                    return default

                if self._head is e:
                    return e.value

                self._remove(e)
                self._insert_head(e)
                return e.value
            return default

    def set(self, k, v, expires=None):
        with self._lock:
            if k in self._cache_content:
                self._remove(self._cache_content[k])

            if len(self._cache_content) >= self._max_size:
                # pop tail
                self._cache_content.pop(self._tail.key)
                tail_pre = self._tail.pre_entry
                self._remove(self._tail)
                self._tail = tail_pre

            e = Entry(k, v, expires or self._expires)
            self._insert_head(e)
            self._cache_content[k] = e

    def delete(self, k):
        with self._lock:
            e = self._cache_content.get(k, None)

            if e is None:
                return False
            else:
                self._cache_content.pop(e.key)
                self._remove(e)
                return not e.expired

    def _insert_head(self, e):
        if not self._head:
            self._head = e
            self._tail = e
            return

        self._head.pre_entry = e
        e.next_entry = self._head
        e.pre_entry = None
        self._head = e

    def _remove(self, e):
        e_pre = e.pre_entry
        e_next = e.next_entry

        if e_pre:
            e_pre.next_entry = e_next
        else:
            self._head = e_next

        if e_next:
            e_next.pre_entry = e_pre
        else:
            self._tail = e_pre

    def __iter__(self):
        entreis = []
        with self._lock:
            entry = self._head
            while entry:
                if not entry.expired:
                    entreis.append(entry)
                entry = entry.next_entry
        for e in entreis:
            yield e.key, e.value


class Entry(object):

    def __init__(self, k, v, expires=None):
        self._key = k
        self._value = v
        self._pre = None
        self._next = None
        self._expire_at = None
        if expires:
            self._expire_at = time.time() + expires

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, k):
        self._key = k

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v

    @property
    def expired(self):
        if self._expire_at is None:
            return False
        return time.time() > self._expire_at

    @property
    def pre_entry(self):
        return self._pre

    @pre_entry.setter
    def pre_entry(self, e):
        self._pre = e

    @property
    def next_entry(self):
        return self._next

    @next_entry.setter
    def next_entry(self, e):
        self._next = e

    def __str__(self):
        return str('%s: %s' % (self._key, self._value))
