import re
from collections import defaultdict

REGISTERS = None


class State:
    def __init__(self, before, opcode, params, after):
        self.before = before
        self.opcode = opcode
        self.params = params
        self.after = after


def addr(reg_a, reg_b, reg_c):
    global REGISTERS
    REGISTERS[reg_c] = REGISTERS[reg_a] + REGISTERS[reg_b]


def addi(reg_a, val_b, reg_c):
    global REGISTERS
    REGISTERS[reg_c] = REGISTERS[reg_a] + val_b


def mulr(reg_a, reg_b, reg_c):
    global REGISTERS
    REGISTERS[reg_c] = REGISTERS[reg_a] * REGISTERS[reg_b]


def muli(reg_a, val_b, reg_c):
    global REGISTERS
    REGISTERS[reg_c] = REGISTERS[reg_a] * val_b


def banr(reg_a, reg_b, reg_c):
    global REGISTERS
    REGISTERS[reg_c] = REGISTERS[reg_a] & REGISTERS[reg_b]


def bani(reg_a, val_b, reg_c):
    global REGISTERS
    REGISTERS[reg_c] = REGISTERS[reg_a] & val_b


def borr(reg_a, reg_b, reg_c):
    global REGISTERS
    REGISTERS[reg_c] = REGISTERS[reg_a] | REGISTERS[reg_b]


def bori(reg_a, val_b, reg_c):
    global REGISTERS
    REGISTERS[reg_c] = REGISTERS[reg_a] | val_b


def setr(reg_a, _, reg_c):
    global REGISTERS
    REGISTERS[reg_c] = REGISTERS[reg_a]


def seti(val_a, _, reg_c):
    global REGISTERS
    REGISTERS[reg_c] = val_a


def gtir(val_a, reg_b, reg_c):
    global REGISTERS
    REGISTERS[reg_c] = 1 if val_a > REGISTERS[reg_b] else 0


def gtri(reg_a, val_b, reg_c):
    global REGISTERS
    REGISTERS[reg_c] = 1 if REGISTERS[reg_a] > val_b else 0


def gtrr(reg_a, reg_b, reg_c):
    global REGISTERS
    REGISTERS[reg_c] = 1 if REGISTERS[reg_a] > REGISTERS[reg_b] else 0


def eqir(val_a, reg_b, reg_c):
    global REGISTERS
    REGISTERS[reg_c] = 1 if val_a == REGISTERS[reg_b] else 0


def eqri(reg_a, val_b, reg_c):
    global REGISTERS
    REGISTERS[reg_c] = 1 if REGISTERS[reg_a] == val_b else 0


def eqrr(reg_a, reg_b, reg_c):
    global REGISTERS
    REGISTERS[reg_c] = 1 if REGISTERS[reg_a] == REGISTERS[reg_b] else 0


def load_states(filename="day_16.txt"):
    states = []
    state_pattern = re.compile(
        r"Before: (?P<before>\[.+\])\n(?P<params>.+)\nAfter:  (?P<after>\[.+\])"
    )
    with open(filename) as input_file:
        lines = input_file.read()
        for state_line in lines[: lines.find("\n\n\n")].split("\n\n"):
            match = state_pattern.search(state_line)
            opcode, *params = map(int, match.group("params").split(" "))
            states.append(
                State(
                    match.group("before"), opcode, params, match.group("after")
                )
            )
        return states


if __name__ == "__main__":
    states = load_states()
    ops = [
        addr,
        addi,
        mulr,
        muli,
        banr,
        bani,
        borr,
        bori,
        setr,
        seti,
        gtir,
        gtri,
        gtrr,
        eqir,
        eqri,
        eqrr,
    ]
    ops_by_states = defaultdict(list)

    for state in states:
        for op in ops:
            REGISTERS = eval(state.before)
            op(*state.params)
            if REGISTERS == eval(state.after):
                ops_by_states[state].append(op)

    print(sum(1 for ops in ops_by_states.values() if len(ops) >= 3))
