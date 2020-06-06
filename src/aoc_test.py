#!/usr/bin/python3

import fileutils

class AocTest(object):
    def __init__(self, day, part, filename, expected_result, extra_args):
        self.day = day
        self.part = part
        self.filename = filename
        self.expected_result = expected_result
        self.extra_args = extra_args
    
    def compare_result(self, actual_result):
        return str(self.expected_result) ==  str(actual_result)
