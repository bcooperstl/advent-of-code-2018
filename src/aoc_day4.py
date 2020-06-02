import aoc_day
import fileutils
import sys
import itertools
from operator import itemgetter

class AocDay4(aoc_day.AocDay):
    def __init__(self):
        aoc_day.AocDay.__init__(self, 4)
    
    def split_to_shifts(self, logs):
        shifts = []
        current_shift = {}
        # log lines: [1518-11-01 00:00] Guard #10 begins shift
        #            [1518-11-01 00:05] falls asleep
        #            [1518-11-01 00:25] wakes up
        #            012345678901234567890123456789
        for log in logs:
            key = log[19:24] # will be "Guard", "falls", or "wakes"
            if key == "Guard":
                if current_shift:
                    shifts.append(current_shift)
                current_shift = {}
                num_substring = log[26:]
                current_shift["GuardId"]=int(num_substring[:num_substring.find(' ')])
            elif key == "falls":
                minute = int(log[15:17])
                if "asleep" in current_shift:
                    current_shift["asleep"].append(minute)
                else:
                    current_shift["asleep"] = [minute]
            elif key == "wakes":
                minute = int(log[15:17])
                if "awake" in current_shift:
                    current_shift["awake"].append(minute)
                else:
                    current_shift["awake"] = [minute]
            else:
                print("Invalid key",key,"in line",log)
                sys.exit()                
        shifts.append(current_shift)        
        return shifts
    
    def calc_guard_summary(self, shifts):
        sorted_shifts = sorted(shifts, key=itemgetter("GuardId"))
        groups = itertools.groupby(sorted_shifts, key=itemgetter("GuardId"))
        summaries = []
        for guardId, items in groups:
            summary = {}
            total_asleep = 0
            frequencies = [0] * 60
            summary["GuardId"] = guardId
            for day in items:
                if "asleep" in day:
                    for (asleep,awake) in zip(day["asleep"],day["awake"]):
                        total_asleep += (awake-asleep)
                        for i in range(asleep, awake):
                            frequencies[i] += 1
            summary["total_asleep"]=total_asleep
            summary["frequencies"]=frequencies
            summaries.append(summary)
        return summaries
    
    def part1(self, filename):
        logs = fileutils.read_as_list_of_strings(filename)
        logs.sort()
        shifts = self.split_to_shifts(logs)
        summaries = self.calc_guard_summary(shifts)
        max_summary = summaries[0]
        for summary in summaries[1:]:
            if summary["total_asleep"] > max_summary["total_asleep"]:
                max_summary = summary
        max_minute = 0
        max_quantity = max_summary["frequencies"][0]
        for i in range(1,60):
            if max_summary["frequencies"][i] > max_quantity:
                max_minute = i
                max_quantity = max_summary["frequencies"][i]
        return max_summary["GuardId"]*max_minute
    