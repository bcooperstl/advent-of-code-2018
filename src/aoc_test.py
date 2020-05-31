#!/usr/bin/python3

import fileutils

class AocTest(object):
    def __init__(self, day, part, filename, expected_result):
        self.day = day
        self.part = part
        self.filename = filename
        self.expected_result = expected_result
    
    def compare_result(self, actual_result):
        return str(self.expected_result) ==  str(actual_result)
