#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `dbus_curio.core.serializer.serialize_list` function.
"""


import sys
import unittest
from dbus_curio.core.serializer import serialize_list


class TestSerializerList(unittest.TestCase):
        
    def test_000_list_int(self):
        signature = b'n'
        expected = b''.join([b'\x04\x00\x00\x00',
                   b'\x01\x00',
                   b'\x02\x03'])
        target = [1, 770]
        actual = b''.join(serialize_list(target, signature))
        self.assertEqual(expected, actual)
        
    def test_001_list_str(self):
        signature = b's'
        expected = b''.join([b'\x17\x00\x00\x00',
                   b'\x05\x00\x00\x00Hello\x00\x00\x00',
                   b'\x06\x00\x00\x00World!\x00'])
        target = ['Hello', "World!"]
        actual = b''.join(serialize_list(target, signature))
        self.assertEqual(expected, actual)