import aoc_day
import fileutils
import sys

class AocDay16(aoc_day.AocDay):
    def __init__(self):
        aoc_day.AocDay.__init__(self, 16)

    opcode_names = ["addr", "addi", "mulr", "muli", "banr", "bani", "borr", "bori", \
                        "setr", "seti", "gtir", "gtri", "gtrr", "eqir", "eqri", "eqrr", ]
    
    def run_all_operations(self, inst, in_reg):
        results = {}
        for opcode in self.opcode_names:
            results[opcode] = getattr(self, opcode)(inst, in_reg)
        return results
    
    def part1(self, filename, extra_args):
        lines = fileutils.read_as_list_of_strings(filename)
        total = 0
        samples = []
        for i in range(0,len(lines)):
            if lines[i][0:6]=="Before":
                sample = {}
                sample["Before"]=[int(val) for val in lines[i][9:-1].split(", ")]
                sample["Inst"]=self.ram_to_inst([int(val) for val in lines[i+1].split(" ")])
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
        for i in self.opcode_names:
            inst_to_opcodes[i]=set()
        
        for i in range(0,len(lines)):
            if lines[i][0:6]=="Before":
                sample = {}
                sample["Before"]=[int(val) for val in lines[i][9:-1].split(", ")]
                sample["Inst"]=self.ram_to_inst([int(val) for val in lines[i+1].split(" ")])
                sample["After"]=[int(val) for val in lines[i+2][9:-1].split(", ")]
                last_after=i+2
                samples.append(sample)
            if i > last_after and len(lines[i]) > 0:
                test_program.append(self.ram_to_inst([int(val) for val in lines[i].split(" ")]))
        
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
            reg = getattr(self, opcode_map[line["opcode"]])(line, reg)
        return reg[0]

    # Convert 4 elements from a list to a CPU instructions
    #   element 1 is opcode
    #   element 2 is input A
    #   element 3 is input B
    #   element 4 is output C
    def ram_to_inst(self, ram):
        return {"opcode":ram[0], "A":ram[1], "B":ram[2], "C":ram[3]}
    
    # addr (add register) stores into register C the result of adding register A and register B.
    def addr(self, inst, in_reg):
        out_reg = in_reg.copy()
        out_reg[inst["C"]] = in_reg[inst["A"]] + in_reg[inst["B"]]
        return out_reg
    
    # addi (add immediate) stores into register C the result of adding register A and value B.
    def addi(self, inst, in_reg):
        out_reg = in_reg.copy()
        out_reg[inst["C"]] = in_reg[inst["A"]] + inst["B"]
        return out_reg
    
    # mulr (multiply register) stores into register C the result of multiplying register A and register B.
    def mulr(self, inst, in_reg):
        out_reg = in_reg.copy()
        out_reg[inst["C"]] = in_reg[inst["A"]] * in_reg[inst["B"]]
        return out_reg

    # muli (multiply immediate) stores into register C the result of multiplying register A and value B.
    def muli(self, inst, in_reg):
        out_reg = in_reg.copy()
        out_reg[inst["C"]] = in_reg[inst["A"]] * inst["B"]
        return out_reg

    # banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
    def banr(self, inst, in_reg):
        out_reg = in_reg.copy()
        out_reg[inst["C"]] = in_reg[inst["A"]] & in_reg[inst["B"]]
        return out_reg

    # bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.
    def bani(self, inst, in_reg):
        out_reg = in_reg.copy()
        out_reg[inst["C"]] = in_reg[inst["A"]] & inst["B"]
        return out_reg

    # borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
    def borr(self, inst, in_reg):
        out_reg = in_reg.copy()
        out_reg[inst["C"]] = in_reg[inst["A"]] | in_reg[inst["B"]]
        return out_reg

    # bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.
    def bori(self, inst, in_reg):
        out_reg = in_reg.copy()
        out_reg[inst["C"]] = in_reg[inst["A"]] | inst["B"]
        return out_reg

    # setr (set register) copies the contents of register A into register C. (Input B is ignored.)
    def setr(self, inst, in_reg):
        out_reg = in_reg.copy()
        out_reg[inst["C"]] = in_reg[inst["A"]]
        return out_reg

    # seti (set immediate) stores value A into register C. (Input B is ignored.)
    def seti(self, inst, in_reg):
        out_reg = in_reg.copy()
        out_reg[inst["C"]] = inst["A"]
        return out_reg

    # gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
    def gtir(self, inst, in_reg):
        out_reg = in_reg.copy()
        if inst["A"] > in_reg[inst["B"]]:
            out_reg[inst["C"]] = 1
        else:
            out_reg[inst["C"]] = 0
        return out_reg

    # gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
    def gtri(self, inst, in_reg):
        out_reg = in_reg.copy()
        if in_reg[inst["A"]] > inst["B"]:
            out_reg[inst["C"]] = 1
        else:
            out_reg[inst["C"]] = 0
        return out_reg

    # gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
    def gtrr(self, inst, in_reg):
        out_reg = in_reg.copy()
        if in_reg[inst["A"]] > in_reg[inst["B"]]:
            out_reg[inst["C"]] = 1
        else:
            out_reg[inst["C"]] = 0
        return out_reg

    # eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
    def eqir(self, inst, in_reg):
        out_reg = in_reg.copy()
        if inst["A"] == in_reg[inst["B"]]:
            out_reg[inst["C"]] = 1
        else:
            out_reg[inst["C"]] = 0
        return out_reg

    # eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
    def eqri(self, inst, in_reg):
        out_reg = in_reg.copy()
        if in_reg[inst["A"]] == inst["B"]:
            out_reg[inst["C"]] = 1
        else:
            out_reg[inst["C"]] = 0
        return out_reg

    # eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
    def eqrr(self, inst, in_reg):
        out_reg = in_reg.copy()
        if in_reg[inst["A"]] == in_reg[inst["B"]]:
            out_reg[inst["C"]] = 1
        else:
            out_reg[inst["C"]] = 0
        return out_reg

