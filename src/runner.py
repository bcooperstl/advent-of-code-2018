#!/usr/bin/python3

import sys
import aoc_days
import aoc_tests

if len(sys.argv) != 4:
    print("Usage: ", sys.argv[0], "day part [filename|\"tests\"")
    sys.exit()

programs = aoc_days.AocDays()
tests = aoc_tests.AocTests()

day = int(sys.argv[1])
part = int(sys.argv[2])
filename = sys.argv[3]

program = programs.get(day)
if program is None:
    print("Day",day,"is not defined")
    sys.exit()

if (filename != "tests"):
    if part == 1:
        result = program.part1(filename)
    elif part == 2:
        result = program.part2(filename)
    else:
        print("Part",part,"is not defined")
        sys.exit()
    print("***Day",day,"Part",part,"for file",filename,"has result",result)
else:
    all_passed=True
    test_summary = []
    for test in tests.filter_tests(day, part):
        if part == 1:
            actual = program.part1(test.filename)
        elif part == 2:
            actual = program.part2(test.filename)
        else:
            print("Part",part,"is not defined")
            sys.exit()
        if actual == test.expected_result:
            test_summary.append("++"+test.filename+" passed with result="+str(actual))
        else:
            test_summary.append("--"+test.filename+" FAILED expected="+str(test.expected_result)+" actual="+str(actual))
    print("\n".join(test_summary))
