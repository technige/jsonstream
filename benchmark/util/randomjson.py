#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2014 Nigel Small
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

import json
from random import choice, randint, seed
from string import printable, digits


class RandomJSONGenerator(object):

    def __init__(self, s=None):
        self.__depth = 0
        if s:
            seed(s)

    @property
    def indent(self):
        return self.__depth * "    "

    def generate_null(self):
        yield 'null'

    def generate_boolean(self):
        yield choice(['true', 'false'])

    def generate_string(self, min_length=3, max_length=100):
        yield json.dumps(''.join(choice(printable) for i in range(randint(min_length, max_length))))

    def generate_integer(self):
        yield choice('123456789') + ''.join(choice(digits) for i in range(randint(0, 8)))

    def generate_float(self):
        yield next(self.generate_integer()) + '.' + ''.join(choice(digits) for i in range(randint(1, 6)))

    def generate_number(self):
        generator = choice([self.generate_integer, self.generate_float])
        for value in generator():
            yield value

    def generate_array(self, depth=2):
        self.__depth += 1
        foo = '[\n' + self.indent
        for i in range(randint(1, 40)):
            yield foo
            if self.__depth <= depth:
                for item in self.generate_collection(depth - 1):
                    yield item
            else:
                for item in self.generate_element():
                    yield item
            foo = ",\n" + self.indent
        self.__depth -= 1
        yield '\n' + self.indent + ']'

    def generate_object(self, depth=2):
        self.__depth += 1
        keys = set()
        for i in range(randint(1, 40)):
            keys.add(next(self.generate_string(max_length=12)))
        foo = '{\n' + self.indent
        for key in keys:
            yield foo
            yield key
            yield ': '
            if self.__depth <= depth:
                for item in self.generate_collection(depth - 1):
                    yield item
            else:
                for item in self.generate_element():
                    yield item
            foo = ",\n" + self.indent
        self.__depth -= 1
        yield '\n' + self.indent + '}'

    def generate_element(self):
        generator = choice([self.generate_null, self.generate_boolean, self.generate_number, self.generate_string])
        for item in generator():
            yield item

    def generate_collection(self, depth):
        generator = choice([self.generate_array, self.generate_object])
        for item in generator(depth):
            yield item

