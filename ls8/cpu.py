"""CPU functionality."""

import sys

LDI = 130
PRN = 71
HLT = 1
MUL = 162
PUSH = 69
POP = 70

SP = 7


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [None] * 256
        self.reg = [0] * 8
        self.pc = 0

    def ram_read(self, ram_index):
        return self.ram[ram_index]

    def ram_write(self, ram_index, ram_val):
        self.ram[ram_index] = ram_val

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        try:
            with open(filename) as f:
                for line in f:

                    # ignore comments
                    comment_split = line.split('#')

                    # remove whitespace
                    num = comment_split[0].strip()

                    # ignore empty lines
                    if num == '':
                        continue

                    val = int(num, 2)
                    self.ram[address] = val
                    address += 1
        except FileNotFoundError:
            print("File not found")
            sys.exit(2)

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            command = self.ram[self.pc]

            if command == LDI:
                index = self.ram_read(self.pc + 1)
                val = self.ram_read(self.pc + 2)
                self.reg[index] = val
                self.pc += 3
                # print(f"LDI -- index: {index}, val: {val}, pc: {self.pc}")

            elif command == PRN:
                index = self.ram_read(self.pc + 1)
                print(self.reg[index])
                # print(f"pc at PRN start: {self.pc}")
                # print(f"pc + 1 at PRN start: {self.pc + 1}")
                self.pc += 2

            elif command == MUL:
                index_one = self.ram_read(self.pc + 1)
                index_two = self.ram_read(self.pc + 2)
                start_val = self.ram_read(index_one)
                mul_val = self.ram_read(index_two)
                self.ram_write(index_one, start_val * mul_val)
                self.pc += 3

            elif command == PUSH:
                index = self.ram_read(self.pc + 1)
                value = self.reg[index]
                self.reg[SP] -= 1
                self.ram_write(self.reg[SP], value)
                self.pc += 2

            elif command == POP:
                index = self.ram_read(self.pc + 1)
                value = self.ram_read(self.reg[SP])
                self.reg[index] = value
                self.reg[SP] += 1
                self.pc += 2

            elif command == HLT:
                running = False

            else:
                print("ERROR: Unknown command")


cpu = CPU()

if len(sys.argv) != 2:
    print("Usage: cpu.py filename")
    sys.exit(1)

filename = sys.argv[1]

cpu.load(filename)
cpu.run()
# cpu.trace()
# for i in range(0, 12):
#     print(f"i: {i}, ram at i: {cpu.ram[i]}")
