"""CPU functionality."""

import sys

LDI = 0b10000010 
PRN = 0b01000111 
MUL = 0b10100010 
PUSH = 0b01000101 
POP = 0b01000110 
HALT = 0b00000001 
CALL = 0b01010000 
RET = 0b00010001 
ADD = 0b10100000 


class CPU:
    """Main CPU class."""


    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8  # R0-R7
        self.ram = [0] * 256
        self.pc =  0
        self.methods = {}
        self.methods[LDI] = self.ldi
        self.methods[PRN] = self.prn
        self.methods[MUL] = self.mul
        self.methods[PUSH] = self.push
        self.methods[POP] = self.pop
        self.methods[CALL] = self.call
        self.methods[RET] = self.ret
        self.methods[ADD] = self.add
        self.SP = 7



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

    def ldi(self):        
        register_num =  self.ram_read(self.pc + 1) # register number
        value =  self.ram_read(self.pc + 2) # value 
        self.reg[register_num] = value

    def prn(self):
        reg_num = self.ram_read(self.pc + 1)
        # print("binary:", bin(self.reg[reg_num]))
        print("decimal:", self.reg[reg_num])

    def mul(self):
        reg1 =  self.ram_read(self.pc + 1) # register number 1
        reg2 =  self.ram_read(self.pc + 2) # register numnber 2
        result = self.reg[reg1] * self.reg[reg2]
        self.reg[reg1] = result

    def push(self):

        self.reg[self.SP] -= 1
        # Get the reg num to push
        reg_num = self.ram_read(self.pc + 1)
        # Get the value to push
        value = self.reg[reg_num]
        # Copy the value to the SP address
        top_of_stack_addr = self.reg[self.SP]
        self.ram_write(top_of_stack_addr, value)

    
    def pop(self):

		# Get reg to pop into
        reg_num = self.ram_read(self.pc + 1)
        # Get the top of stack addr
        top_of_stack_addr = self.reg[self.SP]
        # Get the value at the top of the stack
        value = self.ram_read(top_of_stack_addr)

        # Store the value in the register
        self.reg[reg_num] = value

        # Increment the SP
        self.reg[self.SP] += 1


    def push_value(self, value):
        # Decrement SP
        self.reg[self.SP] -= 1

        # Copy the value to the SP address
        top_of_stack_addr = self.reg[self.SP]
        self.ram[top_of_stack_addr] = value

    def pop_value(self):
        # Get the top of stack addr
        top_of_stack_addr = self.reg[self.SP]

        # Get the value at the top of the stack
        value = self.ram_read(top_of_stack_addr)

        # Increment the SP
        self.reg[self.SP] += 1

        return value

    def call(self):

        next_address = self.pc + 2
        self.SP -= 1
        self.ram[self.SP] = next_address
        # set pc
        reg_num = self.ram_read(self.pc + 1)
        address = self.reg[reg_num]
        self.pc = address

    def ret(self):
        next_address = self.ram[self.SP]
        self.SP += 1
        self.pc = next_address

    def add(self):

        reg1 =  self.ram_read(self.pc + 1) # register number 1
        reg2 =  self.ram_read(self.pc + 2) # register numnber 2
        result = self.reg[reg1] + self.reg[reg2]
        self.reg[reg1] = result


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

            op = self.ram_read(self.pc)
            inst_sets_pc = (op & 16) 

            # print("op", bin(op))

            if op == 0b00000001: # HLT 
                # break
                running = False
            else:
                self.methods[op]()

            count = self.increment_count(op)   
            if op == CALL or op == RET:
                pass
            else:
                self.pc += count

            # if inst_sets_pc !=  0b00010000: 
            # print("PC", self.pc)
            # print("Regs", self.reg)


