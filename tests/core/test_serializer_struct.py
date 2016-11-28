#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `dbus_curio.core.serializer.serialize_struct` function.
"""


import sys
import unittest
from dbus_curio.core.serializer import serialize_struct


class TestSerializerStruct(unittest.TestCase):
        
    def test_000_struct_byte_int(self):
        signature = b'yn'
        expected = b'\x01\x00\x00\x00\x00\x00\x00\x00' + \
                   b'\x02\x03\x00\x00\x00\x00\x00\x00'
        target = (1, 770)
        actual = b''.join(serialize_struct(target, signature))
        self.assertEqual(expected, actual)