#!/usr/bin/python3

import sys
import os

def read_as_list_of_strings(filename):
    if not os.access(filename, os.F_OK):
        print(filename, "is not a valid filename!")
        sys.exit()
    read_file = open(filename, "r")
    file_contents = list(read_file.read().splitlines())
    read_file.close()
    return file_contents

def read_as_split_strings(filename, delimiter, comment_character):
    result = []
    raw_strings = read_as_list_of_strings(filename)
    for line in raw_strings:
        if comment_character is "" or not line.startswith(comment_character):
            result.append(line.split(delimiter))
    return result

def read_as_split_integers(filename, delimiter, comment_character):
    strings = read_as_split_strings(filename, delimiter, comment_character)
    result = [[int(val) for val in string] for string in strings]
    return result
    
def read_as_string(filename):
    return read_as_list_of_strings(filename)[0]

