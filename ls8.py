#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

run_program = None
try:
    run_program = sys.argv[1]
except:
    print("Please enter a program you'd like to run")


cpu = CPU()
f = open(run_program, "r")
# print(f.readlines())
program = []

for x in f:
    line = x.split('#', 1)[0]
    line = line.strip('\n')
    line = int(line, 2)

    program.append(line)

cpu.load(program)
cpu.run()