#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `dbus_curio.core.serializer` module.
"""


import sys
import unittest

from dbus_curio.core.serializer import serialize_msg
from dbus_curio.core.message_header import \
    method_call, method_return, error, signal



class TestSerializer(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_000_serialize_signal(self):
        expected = b'l\x04\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00'
        s = signal('eggs', 'spam', serial=1)
        ss = serialize_msg(s)
        print("\n{}\n{} in {}\n".format(s, expected, ss))
        assert expected in ss
        
