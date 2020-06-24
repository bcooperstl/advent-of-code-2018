import aoc_day
import aoc_assembly
import fileutils
import sys

class AocDay19(aoc_day.AocDay):
    def __init__(self):
        aoc_day.AocDay.__init__(self, 19)

    assembly = aoc_assembly.AocAssembly()
    
    def parse_input(self, lines):
        ip_reg = int(lines[0].split(" ")[1])
        program = []
        for line in lines[1:]:
            values = line.split(" ")
            program.append(self.assembly.ram_to_inst([values[0], int(values[1]), int(values[2]), int(values[3])]))
        return ip_reg, program
    
    def run_program(self, program, registers, ip_reg):
        ip = 0
        while 0 <= ip < len(program):
            registers[ip_reg]=ip
            inst = program[ip]
            #print("IP:",ip,"registers",registers,inst["opcode"],inst["A"],inst["B"],inst["C"])
            registers = self.assembly.run_inst(inst["opcode"], inst, registers)
            #print("   ",registers)
            ip = registers[ip_reg]+1
        return registers
        
    
    def part1(self, filename, extra_args):
        lines = fileutils.read_as_list_of_strings(filename)
        registers = [0, 0, 0, 0, 0, 0]
        ip_reg, program = self.parse_input(lines)
        registers = self.run_program(program, registers, ip_reg)
        print("Final Registers:", registers)
        return registers[0]

    def part2(self, filename, extra_args):
        lines = fileutils.read_as_list_of_strings(filename)
        registers = [1, 0, 0, 0, 0, 0]
        ip_reg, program = self.parse_input(lines)
        registers = self.run_program(program, registers, ip_reg)
        print("Final Registers:", registers)
        return registers[0]

