#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `dbus_curio.core.serializer.serialize_str` function.
"""


import sys
import unittest
from dbus_curio.core.serializer import serialize_str


class TestSerializerStr(unittest.TestCase):

    def test_000_serialize_str_small(self):
        size = b'\x02\x00\x00\x00'
        string = b'eg\x00'
        pad = b'\x00'
        expected = [size, string, pad]
        target = 'eg'
        actual = list(serialize_str(target))
        self.assertEqual(expected, actual)
        self.assertEqual(0, len(b''.join(actual)) % 4)
    
    def test_001_serialize_str_big(self):
        size = b'\x08\x00\x00\x00'
        string = b'eggsspam\x00'
        pad = b'\x00\x00\x00'
        expected = [size, string, pad]
        target = 'eggsspam'
        actual = list(serialize_str(target))
        self.assertEqual(0, len(b''.join(actual)) % 4)
        self.assertEqual(expected, actual)
