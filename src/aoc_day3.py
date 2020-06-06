import aoc_day
import fileutils
import sys
import re

class AocDay3(aoc_day.AocDay):
    def __init__(self):
        aoc_day.AocDay.__init__(self, 3)
    
    # line format is [#1 @ 1,3: 4x4]
    # will extract claimId, startX, startY, width, height
    # will also calculate endX and endY for convenience here
    def parse_input_line(self, line):
        regex = "#(\\d+) @ (\\d+),(\\d+): (\\d+)x(\\d+)"
        ret = {}
        parsed_line = re.search(regex, line)
        if parsed_line:
            ret["claimId"]=int(parsed_line.group(1))
            ret["startX"]=int(parsed_line.group(2))
            ret["startY"]=int(parsed_line.group(3))
            ret["width"]=int(parsed_line.group(4))
            ret["height"]=int(parsed_line.group(5))
            ret["endX"]=ret["startX"]+ret["width"]-1
            ret["endY"]=ret["startY"]+ret["height"]-1
        else:
            print("No match found")
        return ret
    
    def apply_claim(self, claim, one_claim_points, multi_claim_points):
        for x in range(claim["startX"], claim["endX"]+1):
            for y in range(claim["startY"], claim["endY"]+1):
                if (not x in multi_claim_points) or (not y in multi_claim_points[x]):
                    if (x in one_claim_points) and (y in one_claim_points[x]): # need to move x,y to multi_claim_points
                        one_claim_points[x].remove(y)
                        if not x in multi_claim_points:
                            multi_claim_points[x]=[y]
                        else:
                            multi_claim_points[x].append(y)
                    else:
                        if not x in one_claim_points:
                            one_claim_points[x]=[y]
                        else:
                            one_claim_points[x].append(y)
    
    def part1(self, filename, extra_args):
        claim_lines = fileutils.read_as_list_of_strings(filename)
        one_claim_points = {}
        multi_claim_points = {}
        for claim_line in claim_lines:
            claim = self.parse_input_line(claim_line)
            #print("Claim:",claim)
            self.apply_claim(claim, one_claim_points, multi_claim_points)
        sum = 0
        for x in multi_claim_points:
            sum += len(multi_claim_points[x])
        return sum
    
    def claims_overlap(self, claim1, claim2):
        # using brute force here because I would need to for a certain failing case. check for all points in claim1 if they are in claim2
        for x in range(claim1["startX"], claim1["endX"]+1):
            for y in range(claim1["startY"], claim1["endY"]+1):
                if claim2["startX"] <= x <= claim2["endX"] and \
                   claim2["startY"] <= y <= claim2["endY"]:
                    return True

        return False
    
    def part2(self, filename, extra_args):
        claim_lines = fileutils.read_as_list_of_strings(filename)
        claims = []
        for claim_line in claim_lines:
            claims.append(self.parse_input_line(claim_line))
        for claim1 in claims:
            overlap = False
            for claim2 in claims:
                if claim1["claimId"] != claim2["claimId"]:
                    if self.claims_overlap(claim1, claim2):
                        overlap = True
                if overlap == True: # short circuit out of here
                    break
            if not overlap:
                print("Claim",claim1["claimId"],"does not overlap any others")
                return claim1["claimId"]
        return 0
# TODO: Check lines 30 and 896 for why they don't compare right