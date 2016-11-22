#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `dbus_curio.core.serializer.break_signature` function.
"""

import sys
import unittest

from dbus_curio.core.serializer import break_signature


class TestBreakSignature(unittest.TestCase):

    def test_000_break_header_signature(self):
        expected = [b'y', b'y', b'y', b'y', b'u', b'u', b'a(yv)']
        target = b'yyyyuua(yv)'
        actual = [x for x in break_signature(target)]
        self.assertEqual(expected, actual)
