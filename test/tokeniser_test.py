#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2012-2014 Nigel Small
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import unicode_literals

from . import jsonstream_import

Tokeniser = jsonstream_import("Tokeniser")
AwaitingData = jsonstream_import("AwaitingData")
EndOfStream = jsonstream_import("EndOfStream")
UnexpectedCharacter = jsonstream_import("UnexpectedCharacter")


def test_null():
    tokeniser = Tokeniser()
    tokeniser.write('null')
    tokeniser.close()
    assert tokeniser.read_token() == ('null', None)


def test_true():
    tokeniser = Tokeniser()
    tokeniser.write('true')
    tokeniser.close()
    assert tokeniser.read_token() == ('true', True)


def test_false():
    tokeniser = Tokeniser()
    tokeniser.write('false')
    tokeniser.close()
    assert tokeniser.read_token() == ('false', False)


def test_two_part_boolean_value():
    tokeniser = Tokeniser()
    tokeniser.write('fal')
    try:
        tokeniser.read_token()
    except AwaitingData:
        assert True
    else:
        assert False
    tokeniser.write('se')
    tokeniser.close()
    assert tokeniser.read_token() == ('false', False)


def test_broken_boolean_value():
    tokeniser = Tokeniser()
    tokeniser.write('fal')
    tokeniser.close()
    try:
        tokeniser.read_token()
    except EndOfStream:
        assert True
    else:
        assert False


def test_unknown_value():
    tokeniser = Tokeniser()
    tokeniser.write('xyz')
    tokeniser.close()
    try:
        tokeniser.read_token()
    except UnexpectedCharacter:
        assert True
    else:
        assert False


def test_misleading_value():
    tokeniser = Tokeniser()
    tokeniser.write('foo')
    tokeniser.close()
    try:
        tokeniser.read_token()
    except UnexpectedCharacter:
        assert True
    else:
        assert False


def test_string():
    tokeniser = Tokeniser()
    tokeniser.write('"foo"')
    tokeniser.close()
    assert tokeniser.read_token() == ('"foo"', u"foo")


def test_two_part_string_value():
    tokeniser = Tokeniser()
    tokeniser.write('"foo')
    try:
        tokeniser.read_token()
    except AwaitingData:
        assert True
    else:
        assert False
    tokeniser.write('bar"')
    tokeniser.close()
    assert tokeniser.read_token() == ('"foobar"', u"foobar")


def test_broken_string_value():
    tokeniser = Tokeniser()
    tokeniser.write('"foo')
    tokeniser.close()
    try:
        tokeniser.read_token()
    except EndOfStream:
        assert True
    else:
        assert False


def test_broken_string_value_with_trailing_escape():
    tokeniser = Tokeniser()
    tokeniser.write('"foo\\')
    tokeniser.close()
    try:
        tokeniser.read_token()
    except EndOfStream:
        assert True
    else:
        assert False


def test_broken_string_value_with_hanging_escape():
    tokeniser = Tokeniser()
    tokeniser.write('"foo\\')
    try:
        tokeniser.read_token()
    except AwaitingData:
        assert True
    else:
        assert False
    tokeniser.close()


def test_string_with_escaped_characters():
    tokeniser = Tokeniser()
    tokeniser.write('"\\"/\\\\\\b\\f\\n\\r\\t"')
    tokeniser.close()
    assert tokeniser.read_token() == ('"\\"/\\\\\\b\\f\\n\\r\\t"',
                                      u"\"/\\\b\f\n\r\t")


def test_string_with_illegal_escape():
    tokeniser = Tokeniser()
    tokeniser.write('"foo\\xbar"')
    tokeniser.close()
    try:
        tokeniser.read_token()
    except UnexpectedCharacter:
        assert True
    else:
        assert False


def test_string_with_unicode_char():
    tokeniser = Tokeniser()
    tokeniser.write('"\\u00a3100"')
    tokeniser.close()
    assert tokeniser.read_token() == ('"\\u00a3100"', u"\xa3100")


def test_string_array():
    tokeniser = Tokeniser()
    tokeniser.write('["foo", "bar", "baz"]')
    tokeniser.close()
    assert tokeniser.read_token() == ('[', None)
    assert tokeniser.read_token() == ('"foo"', u"foo")
    assert tokeniser.read_token() == (',', None)
    assert tokeniser.read_token() == ('"bar"', u"bar")
    assert tokeniser.read_token() == (',', None)
    assert tokeniser.read_token() == ('"baz"', u"baz")
    assert tokeniser.read_token() == (']', None)


def test_int():
    tokeniser = Tokeniser()
    tokeniser.write('42')
    tokeniser.close()
    assert tokeniser.read_token() == ('42', 42)


def test_negative_int():
    tokeniser = Tokeniser()
    tokeniser.write('-42')
    tokeniser.close()
    assert tokeniser.read_token() == ('-42', -42)

def test_float():
    tokeniser = Tokeniser()
    tokeniser.write('3.14')
    tokeniser.close()
    assert tokeniser.read_token() == ('3.14', 3.14)


def test_negative_float():
    tokeniser = Tokeniser()
    tokeniser.write('-3.14')
    tokeniser.close()
    assert tokeniser.read_token() == ('-3.14', -3.14)


def test_int_comma_int():
    tokeniser = Tokeniser()
    tokeniser.write('42, 76')
    tokeniser.close()
    assert tokeniser.read_token() == ('42', 42)
    assert tokeniser.read_token() == (',', None)
    assert tokeniser.read_token() == ('76', 76)


def test_int_comma_string():
    tokeniser = Tokeniser()
    tokeniser.write('42, "meaning of life"')
    tokeniser.close()
    assert tokeniser.read_token() == ('42', 42)
    assert tokeniser.read_token() == (',', None)
    assert tokeniser.read_token() == ('"meaning of life"', "meaning of life")
