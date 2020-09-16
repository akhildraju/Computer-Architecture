"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8  # R0-R7
        self.ram = [0] * 256
        self.pc =  0

    def load_file(self, filename):
        try:
            address = 0
            memory = [0] * 256


            with open(filename) as f:
                for line in f:
                    t = line.split('#')
                    n = t[0].strip()

                    if n == '':
                        continue

                    try:
                        n = int(n, 2)
                    except ValueError:
                        print(f"Invalid number '{n}'")
                        sys.exit(1)

                    memory[address] = n
                    address += 1

            return memory

        except FileNotFoundError:
            print(f"File not found: {filename}")
            return None
        




    def load(self, filename):
        """Load a program into memory."""

        self.ram = self.load_file(filename)
        # print(self.ram)

        # address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def ram_read(self, num):
        return self.ram[num]
    
    def ram_write(self, num, value):
        self.ram[num] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def increment_count(self, op):
        count = ((op & 11000000) >> 6) + 1
        return count

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):

        running = True

        while running:

            ir = self.pc 
            op = self.ram_read(ir)
            count = self.increment_count(op)
            # print("LR", ir, "OP", bin(op), "count", count)
            # print("reg1", self.reg[0], "reg2", self.reg[1])


            if op == 0b10000010: # LDI 
                reg =  self.ram_read(ir + 1) # register number
                value =  self.ram_read(ir + 2) # value 
                self.reg[reg] = value
                self.pc += count

            elif op == 0b01000111: # PRN 
                reg_num = self.ram_read(ir + 1)
                print("binary:", bin(self.reg[reg_num]))
                print("decimal:", self.reg[reg_num])
                self.pc += count

            elif op == 0b10100010: # MUL Get values from 2 registers  and multiply and store the results in the 1st register
                reg1 =  self.ram_read(ir + 1) # register number 1
                reg2 =  self.ram_read(ir + 2) # register numnber 2
                # print("reg1 index", reg1, "reg2 index", reg2)
                result = self.reg[reg1] * self.reg[reg2]
                # print("Result", result)
                self.reg[reg1] = result
                self.pc += count

            elif op == 0b00000001: # HLT 
                running = False
            else:
                self.pc += count
                continue


