import aoc_day
import fileutils
import sys
from collections import defaultdict

class AocDay7(aoc_day.AocDay):
    def __init__(self):
        aoc_day.AocDay.__init__(self, 7)

    def part1(self, filename, extra_args):
        instructions = fileutils.read_as_split_strings(filename, " ","") # space is delimiter, no comments
        steps = []
        all_values = []
        requirements = defaultdict(list)
        # example is "Step C must be finished before step A can begin."
        #  Will store requirements[A].append(C) based on that
        #  That way the keys define the steps and the values define the dependencies
        for instruction in instructions:
            all_values.append(instruction[1])
            all_values.append(instruction[7])
            requirements[instruction[7]].append(instruction[1])
        all_values=list(set(all_values))
        while all_values:
            next = min(list(filter(lambda x: requirements[x] == [], all_values)))
            print("Next value:",next)
            steps.append(next)
            del requirements[next]
            for requirement in requirements.values(): # it's been satisfied. remove it from the dependencies
                if next in requirement:
                    requirement.remove(next)
            all_values.remove(next)
        return ''.join(steps)

    def part2(self, filename, extra_args):
        instructions = fileutils.read_as_split_strings(filename, " ","") # space is delimiter, no comments
        num_workers = int(extra_args[0])
        extra_time = int(extra_args[1])
        steps = []
        requirements = defaultdict(list)
        workers = []
        for i in range(0,num_workers):
            workers.append({"id":i,"job":"","time_free":0})
        
        time = 0
        # example is "Step C must be finished before step A can begin."
        #  Will store requirements[A].append(C) based on that
        #  That way the keys define the steps and the values define the dependencies
        all_values = {}
        for instruction in instructions:
            for c in [instruction[1], instruction[7]]:
                if not c in all_values:
                    all_values[c]={"letter":c, "time":ord(c)-ord('A')+1+extra_time}
            requirements[instruction[7]].append(instruction[1])
        print("All values",all_values)
        print("Requirements", requirements)
        num_assigned = 0
        while all_values or num_assigned>0:
            print("Time:",time)
            # first mark workers current jobs as done
            for worker in workers:
                if worker["job"] != "" and time == worker["time_free"]:
                    print("Worker",worker["id"],"finished job",worker["job"],"at",time,"seconds")
                    steps.append(worker["job"])
                    del requirements[worker["job"]]
                    for requirement in requirements.values(): # it's been satisfied. remove it from the dependencies
                        if worker["job"] in requirement:
                            requirement.remove(worker["job"])
                    worker["job"]=""
                    num_assigned -= 1

            # find available jobs and assign them to any free workers
            avail_steps = sorted(list(filter(lambda x: requirements[x] == [], all_values.keys())))
            if avail_steps:
                print("Available steps:",avail_steps)
            for step in avail_steps:
                for worker in workers:
                    if worker["job"]=="":
                        finish_time=time+all_values[step]["time"]
                        print("Worker",worker["id"],"assigned job",step,"at",time,"seconds to finish at",finish_time,"seconds")
                        worker["job"]=step
                        worker["time_free"]=finish_time
                        del all_values[step]
                        num_assigned += 1
                        break #do not assign this step to multiple wokers
            time += 1
        return time-1
