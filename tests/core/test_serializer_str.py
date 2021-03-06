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
    
    def test_001_serialize_str_big(self):
        size = b'\x08\x00\x00\x00'
        string = b'eggsspam\x00'
        pad = b'\x00'
        expected = [size, string, pad]
        target = 'eggsspam'
        actual = list(serialize_str(target))
        self.assertEqual(expected, actual)

    def test_003_serialize_string(self):
        expected = [b'\x0b\x00\x00\x00', b'Hello World\x00', b'']
        target = 'Hello World'
        actual = list(serialize_str(target))
        self.assertEqual(expected, actual)

    def test_004_serialize_hello(self):
        expected = [b'\x05\x00\x00\x00', b'Hello\x00', b'\x00\x00']
        target = 'Hello'
        actual = list(serialize_str(target))
        self.assertEqual(expected, actual)

    def test_005_serialize_world(self):
        expected = [b'\x06\x00\x00\x00', b'World!\x00', b'\x00']
        target = 'World!'
        actual = list(serialize_str(target))
        self.assertEqual(expected, actual)
