import fileutils
import sys

class AocAssembly(object):
    opcode_names = ["addr", "addi", "mulr", "muli", "banr", "bani", "borr", "bori", \
                    "setr", "seti", "gtir", "gtri", "gtrr", "eqir", "eqri", "eqrr", ]
    
    # Convert 4 elements from a list to a CPU instructions
    #   element 1 is opcode
    #   element 2 is input A
    #   element 3 is input B
    #   element 4 is output C
    def ram_to_inst(self, ram):
        return {"opcode":ram[0], "A":ram[1], "B":ram[2], "C":ram[3]}
    
    def run_inst(self, name, inst, in_reg):
        return getattr(self, name)(inst, in_reg)
    
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
    