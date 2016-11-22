#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `dbus_curio.core.signature.end_of` function.
"""


import sys
import unittest
from dbus_curio.core.signature import end_of_struct, end_of_array


class TestEndOfStruct(unittest.TestCase):
    def test_000_end_of_struct(self):
        expected = b'iou)'
        target = b'iou)oui'
        actual = end_of_struct(target)
        self.assertEqual(expected, actual)

    def test_001_end_of_first_struct(self):
        expected = b'iou)'
        target = b'iou)o(ui)'
        actual = end_of_struct(target)
        self.assertEqual(expected, actual)

    def test_002_end_of_inside_struct(self):
        expected = b'iou)'
        target = b'iou)oui)'
        actual = end_of_struct(target)
        self.assertEqual(expected, actual)

    def test_003_end_of_contain_struct(self):
        expected = b'io(ui)ou)'
        target = b'io(ui)ou)oui)'
        actual = end_of_struct(target)
        self.assertEqual(expected, actual)


class TestEndOfArray(unittest.TestCase):
    def test_000_end_of_array(self):
        expected = b'b'
        target = b'biou'
        actual = end_of_array(target)
        self.assertEqual(expected, actual)

    def test_001_end_of_array_dict(self):
        expected = b'{iou}'
        target = b'{iou}o(ui)'
        actual = end_of_array(target)
        self.assertEqual(expected, actual)

    def test_002_end_of_array_of_array(self):
        expected = b'ab'
        target = b'abaiaoau'
        actual = end_of_array(target)
        self.assertEqual(expected, actual)

    def test_003_end_of_array_of_array_dict(self):
        expected = b'a{is}'
        target = b'a{is}baiaoau'
        actual = end_of_array(target)
        self.assertEqual(expected, actual)

    def test_004_end_of_array_of_array_of_struct_with_array_of_dict(self):
        expected = b'a(a{is})'
        target = b'a(a{is})baiaoau'
        actual = end_of_array(target)
        self.assertEqual(expected, actual)
