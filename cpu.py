"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        #hold 256 bytes of memory
        self.ram = [0] * 256
        # 8 general-purpose registers
        self.reg = [0] * 8
        self.pc = 0
        # self.reg = self.ram[self.pc]
        self.sp = 7
        self.FL = 0b00000000

    def ram_read(self, read_address):
        #read the value at the read_address. Not sure if this is right...
        return self.ram[read_address]

    def ram_write(self, write_value, write_address):
        #accept the value to write & address to write it to
        pass

    def load(self, program):
        """Load a program into memory."""
        # print("Program is: ", program)
        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == 'CMP':
            if self.reg[reg_a] < self.reg[reg_b]:
                self.FL = 0b00000100
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.FL = 0b00000010
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.FL = 0b00000001
            else:
                self.FL = 0b00000000

        elif op == 'AND':
            andVal = reg_a & reg_b
            self.reg[reg_a] = andVal

        elif op == 'OR':
            orVal = reg_a | reg_b
            self.reg[reg_a] = orVal

        elif op == 'XOR':
            xVal = reg_a ^ reg_b
            self.reg[reg_a] = xVal

        elif op == 'NOT':
            self.reg[reg_a] = 0b11111111 - self.reg[reg_a]

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.FL,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
    # , operand_a=None, operand_b=None
        """Run the CPU."""
        print(self.ram)
        while True:
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)
            command = self.ram[self.pc]

            if command == 0b00000001:
                # return False
                sys.exit(0)

                #LDI
            elif command == 0b10000010:
                self.reg[operand_a] = operand_b
                # print('LDI while at ', self.reg)
                self.pc += 3

                #PRN
            elif command == 0b01000111:
                print("Printing: ", self.reg[operand_a])
                self.pc += 2

                #MUL
            elif command == 0b10100010:
                # print(f"Multiplying at ", self.reg)
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3


                #POP
            elif command == 0b01000110:
                reg_index = self.ram[self.pc+1]
                reg_val = self.ram[self.reg[self.sp]]
                
                #copy the value from the address pointed to by SP to the given register
                self.reg[reg_index] = reg_val

                self.reg[self.sp] += 1
                self.pc += 2


                #PUSH
            elif command == 0b01000101:
                reg_index = self.ram[self.pc+1]
                reg_val = self.reg[reg_index]
                # copied_val = self.ram[operand_a]
                
                #decrement the SP....?why am I decrementing the value of the register at sp? thought I'm supposed to decrement the SP?
                self.reg[self.sp] -= 1

                #copy the value in the given register to the address pointed to by SP
                self.ram[self.reg[self.sp]] = reg_val
                self.pc += 2

                #CMP
            elif command == 0b10100111:
                self.alu("CMP", operand_a, operand_b)
                self.pc += 3

                #JMP
            elif command == 0b01010100:
                given_register = self.ram[self.pc+1]
                self.pc = self.reg[given_register]

                #JEQ
            elif command == 0b01010101:
                if self.FL & 1 == 1:
                    given_register = self.ram[self.pc+1]
                    self.pc = self.reg[given_register]
                else:
                    self.pc += 2

                #JNE
            elif command == 0b01010110:
                if self.FL & 1 == 0:
                    given_register = self.ram[self.pc+1]
                    self.pc = self.reg[given_register]
                else:
                    self.pc += 2

            #STRETCH
                #AND
            elif command == 0b10101000:
                self.alu('AND', operand_a, operand_b)
                self.pc += 3

                #OR
            elif command == 0b10101010:
                self.alu('OR', operand_a, operand_b)
                self.pc += 3

                #XOR
            elif command == 0b10101011:
                self.alu('XOR', operand_a, operand_b)
                self.pc += 3

                #NOT
            elif command == 0b01101001:
                self.alu('NOT', operand_a)
                self.pc += 2

            else:
                print(f"Sorry I couldn't find that command: {command}, {self.pc}")
                sys.exit(0)


                #I have to go through step by step to see where it's breaking