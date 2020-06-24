import aoc_day
import aoc_assembly
import fileutils
import sys

class AocDay16(aoc_day.AocDay):
    def __init__(self):
        aoc_day.AocDay.__init__(self, 16)

    assembly = aoc_assembly.AocAssembly()
    
    def run_all_operations(self, inst, in_reg):
        results = {}
        for opcode_name in self.assembly.opcode_names:
            results[opcode_name] = self.assembly.run_inst(opcode_name, inst, in_reg)
        return results
    
    def part1(self, filename, extra_args):
        lines = fileutils.read_as_list_of_strings(filename)
        total = 0
        samples = []
        for i in range(0,len(lines)):
            if lines[i][0:6]=="Before":
                sample = {}
                sample["Before"]=[int(val) for val in lines[i][9:-1].split(", ")]
                sample["Inst"]=self.assembly.ram_to_inst([int(val) for val in lines[i+1].split(" ")])
                sample["After"]=[int(val) for val in lines[i+2][9:-1].split(", ")]
                samples.append(sample)
        for sample in samples:
            sample["results"]=self.run_all_operations(sample["Inst"], sample["Before"])
            sample["matching"]=[]
            for result in sample["results"].items():
                if result[1]==sample["After"]:
                    sample["matching"].append(result[0])
            if len(sample["matching"]) >= 3:
                total+=1
        return total
    
    def part2(self, filename, extra_args):
        lines = fileutils.read_as_list_of_strings(filename)
        last_after = -1
        samples = []
        test_program = []
        
        opcodes_to_inst = {}
        inst_to_opcodes = {}
        
        opcode_map = {}
        for i in range(0,16):
            opcodes_to_inst[i]=set()
            opcode_map[i]=None
        for i in self.assembly.opcode_names:
            inst_to_opcodes[i]=set()
        
        for i in range(0,len(lines)):
            if lines[i][0:6]=="Before":
                sample = {}
                sample["Before"]=[int(val) for val in lines[i][9:-1].split(", ")]
                sample["Inst"]=self.assembly.ram_to_inst([int(val) for val in lines[i+1].split(" ")])
                sample["After"]=[int(val) for val in lines[i+2][9:-1].split(", ")]
                last_after=i+2
                samples.append(sample)
            if i > last_after and len(lines[i]) > 0:
                test_program.append(self.assembly.ram_to_inst([int(val) for val in lines[i].split(" ")]))
        
        for sample in samples:
            sample["results"]=self.run_all_operations(sample["Inst"], sample["Before"])
            sample["matching"]=[]
            for result in sample["results"].items():
                if result[1]==sample["After"]:
                    opcodes_to_inst[sample["Inst"]["opcode"]].add(result[0])
                    inst_to_opcodes[result[0]].add(sample["Inst"]["opcode"])
        
        print(opcodes_to_inst)
        print(inst_to_opcodes)
        
        while None in opcode_map.values():
            #opcodes first
            for opcode, instructions in opcodes_to_inst.items():
                if len(instructions) == 1:
                    instruction = next(iter(instructions))
                    print("Setting opcode",opcode,"to inst",instruction,"from opcodes_to_inst")
                    opcode_map[opcode]=instruction
                    print("  Clearing opcode",opcode)
                    print("  Clearing instruction",instruction)
                    opcodes_to_inst[opcode]=set()
                    inst_to_opcodes[instruction]=set()
                    for i,o in inst_to_opcodes.items():
                        if opcode in o:
                            print("  Removing opcode",opcode,"from instruction",i)
                            o.remove(opcode)
                    for o,i in opcodes_to_inst.items():
                        if instruction in i:
                            print("  Removing instruction",instruction,"from opcode",o)
                            i.remove(instruction)
                    #print(opcodes_to_inst)
                    #print(inst_to_opcodes)
            #instructions second
            for instruction, opcodes in inst_to_opcodes.items():
                if len(opcodes) == 1:
                    opcode = next(iter(opcodes))
                    print("Setting opcode",opcode,"to inst",instruction,"from inst_to_opcodes")
                    opcode_map[opcode]=instruction
                    print("  Clearing opcode",opcode)
                    print("  Clearing instruction",instruction)
                    opcodes_to_inst[opcode]=set()
                    inst_to_opcodes[instruction]=set()
                    for i,o in inst_to_opcodes.items():
                        if opcode in o:
                            print("  Removing opcode",opcode,"from instruction",i)
                            o.remove(opcode)
                    for o,i in opcodes_to_inst.items():
                        if instruction in i:
                            print("  Removing instruction",instruction,"from opcode",o)
                            i.remove(instruction)
                    #print(opcodes_to_inst)
                    #print(inst_to_opcodes)
        
        print(opcode_map)
        #print(opcodes_to_inst)
        #print(inst_to_opcodes)

        reg = [0,0,0,0]
        for line in test_program:
            reg = self.assembly.run_inst(opcode_map[line["opcode"]], line, reg)
        return reg[0]

