#!/usr/bin/python3

import aoc_test, fileutils

TEST_DIR = "../test/"
TEST_INDEX_FILE = TEST_DIR+"test_index.txt"

class AocTests(object):
    def __init__(self):
        self.tests = []
        self.load_tests()
        
    def load_tests(self):
        test_list = fileutils.read_as_split_strings(TEST_INDEX_FILE, ",", "#") # CSV file with comments starting with #
        for test in test_list:
            day = int(test[0])
            part = int(test[1])
            expected = int(test[3])
            self.tests.append(aoc_test.AocTest(day, part, TEST_DIR+test[2], expected))
    
    def filter_tests(self, day, part):
        return [test for test in self.tests if test.day == day and test.part == part]

if __name__ == '__main__':
    tests = AocTests()
    for test in tests.tests:
        print("Day", test.day, "Part", test.part, "Filename", test.filename, "Expected", test.expected_result)
