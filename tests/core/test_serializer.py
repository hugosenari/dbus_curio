#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `dbus_curio.core.serializer.serialize` function.


Total 310 bytes

HEADER
    BYTE                    \x6c
    BYTE                    \x04
    BYTE                    \x01
    BYTE                    \x01
    UINT32                  \x60\x00\x00\x00
    UINT32                  \x40\x00\x00\x00
    ARRAY   
        SIZE                \x72\x00\x00\x00
        STRUCT  
            BYTE                \x08
            PADD                \x01\x67\x00
            SIGNATURE   
                SIZE                \x0c
                VAL                 \x74\x73\x6f\x67\x79\x62\x6e\x71\x69\x75\x78\x64\x00
                PADD                \x00\x00\x00\x00\x00\x00
        STRUCT  
            BYTE                \x01
            PADD                \x01\x6f\x00
            STRING  
                SIZE                \x10\x00\x00\x00
                VAL                 \x2f\x61\x61\x61\x61\x61\x61\x61\x2f\x61\x61\x61\x61\x61\x61\x61\x00
                PADD                \x00\x00\x00\x00\x00\x00\x00
        STRUCT  
            BYTE                \x03
            PADD                \x01\x73\x00
            STRING  
                SIZE                \x12\x00\x00\x00
                VAL                 \x63\x63\x63\x63\x63\x63\x63\x63\x63\x63\x63\x63\x63\x63\x63\x63\x63\x63\x00    
                PADD                \x00\x00\x00\x00\x00
        STRUCT  
            BYTE                \x02
            PADD                \x01\x73\x00
            STRING  
                SIZE                \x11\x00\x00\x00
                VAL                 \x62\x62\x62\x62\x62\x62\x62\x62\x62\x2e\x62\x62\x62\x62\x62\x62\x62\x00
                PADD                \x00\x00\x00\x00\x00\x00

BODY        
    UINT64                  \xff\xff\xff\xff\xff\xff\xff\xff
    STRING  
        SIZE                    \x10\x00\x00\x00
        VAL                     \x74\x68\x69\x73\x20\x69\x73\x20\x61\x20\x73\x74\x72\x69\x6e\x67\x00
        PADD                    \x00\x00\x00
    PATH    
        SIZE                    \x0f\x00\x00\x00
        VAL                     \x2f\x74\x68\x69\x73\x2f\x69\x73\x2f\x61\x2f\x70\x61\x74\x68\x00
    SIGN    
        SIZE                    \x03
        VAL                     \x73\x61\x64\x00
    BYTE                    \x2a
    PAD                     \x00\x00
    BOOL                    \x01\x00\x00\x00
    INT16                   \xd6\xff
    UINT16                  \x60\xea
    INT32                   \xd4\xff\xff\xff
    UINT32                  \xa0\x86\x01\x00
    INT                     \x00\x00\x00\x00\x00\x00\x00\x00
    UINT                    \xf8\xff\xff\xff\x00\x00\x00\x00
    DOUB                    \x00\x40\x45\x40

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
                    b'\x00\x00\x00\x00']
        target = 'Hello World'
        actual = list(serialize(b's', b'l', target))
        self.assertEqual(expected, actual)

    def test_010_serialize_path(self):
        expected = [b'\x0b\x00\x00\x00', b'Hello World\x00',
                    b'\x00\x00\x00\x00']
        target = 'Hello World'
        actual = list(serialize(b'o', b'l', target))
        self.assertEqual(expected, actual)

    def test_011_serialize_signature(self):
        expected = [b'\x0b', b'Hello World\x00',
                    b'\x00\x00\x00\x00']
        target = 'Hello World'
        actual = list(serialize(b'g', b'l', target))
        self.assertEqual(expected, actual)
