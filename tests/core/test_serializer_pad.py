#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `dbus_curio.core.serializer.pad` function.
"""


import sys
import unittest
from dbus_curio.core.serializer import pad


class TestSerializerPad(unittest.TestCase):
        
    def test_000_pad_empty(self):
        expected = b''
        target = b''
        actual = pad(len(target))
        self.assertEqual(expected, actual)
        
    def test_001_pad_one(self):
        expected = b'\x01\x00\x00\x00'
        target = b'\x01'
        actual = target + pad(len(target))
        self.assertEqual(expected, actual)
        
    def test_002_pad_more(self):
        expected = b'\x01\x02\x03\x04\x05\x00\x00\x00'
        target = b'\x01\x02\x03\x04\x05'
        actual = target + pad(len(target))
        self.assertEqual(expected, actual)