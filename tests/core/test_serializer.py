#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `dbus_curio.core.serializer.serialize` function.
"""

import sys
import unittest

from dbus_curio.core.serializer import serialize


class TestSerializer(unittest.TestCase):

    def test_000_serialize_byte(self):
        expected = [b'\x04']
        target = 4
        actual = list(serialize(b'y', b'l', target))
        self.assertEqual(expected, actual)

    def test_001_serialize_bool(self):
        expected = [b'\x01\x00\x00\x00']
        target = True
        actual = list(serialize(b'b', b'l', target))
        self.assertEqual(expected, actual)

    def test_002_serialize_int16(self):
        expected = [b'\xfc\xff']
        target = -4
        actual = list(serialize(b'n', b'l', target))
        self.assertEqual(expected, actual)

    def test_003_serialize_uint16(self):
        expected = [b'\x04\x00']
        target = 4
        actual = list(serialize(b'q', b'l', target))
        self.assertEqual(expected, actual)

    def test_004_serialize_int32(self):
        expected = [b'\x04\x00\x00\x00']
        target = 4
        actual = list(serialize(b'i', b'l', target))
        self.assertEqual(expected, actual)

    def test_005_serialize_uint32(self):
        expected = [b'\x04\x00\x00\x00']
        target = 4
        actual = list(serialize(b'u', b'l', target))
        self.assertEqual(expected, actual)

    def test_006_serialize_int64(self):
        expected = [b'\x04\x00\x00\x00\x00\x00\x00\x00']
        target = 4
        actual = list(serialize(b'x', b'l', target))
        self.assertEqual(expected, actual)

    def test_007_serialize_uint64(self):
        expected = [b'\x04\x00\x00\x00\x00\x00\x00\x00']
        target = 4
        actual = list(serialize(b't', b'l', target))
        self.assertEqual(expected, actual)

    def test_008_serialize_double(self):
        expected = [b'\x00\x00\x00\x00\x00\x00\x10@']
        target = 4.0
        actual = list(serialize(b'd', b'l', target))
        self.assertEqual(expected, actual)

    def test_009_serialize_string(self):
        expected = [b'\x0b\x00\x00\x00', b'Hello World\x00',
                    b'\x00\x00\x00']
        target = 'Hello World'
        actual = list(serialize(b's', b'l', target))
        self.assertEqual(expected, actual)

    def test_010_serialize_path(self):
        expected = [b'\x0b\x00\x00\x00', b'Hello World\x00',
                    b'\x00\x00\x00']
        target = 'Hello World'
        actual = list(serialize(b'o', b'l', target))
        self.assertEqual(expected, actual)

    def test_011_serialize_signature(self):
        expected = [b'\x0b', b'Hello World\x00', b'']
        target = 'Hello World'
        actual = list(serialize(b'g', b'l', target))
        self.assertEqual(expected, actual)
