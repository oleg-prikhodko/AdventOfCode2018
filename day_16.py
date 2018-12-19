import re
from collections import defaultdict, Counter

REGISTERS = None


class State:
    def __init__(self, before, opcode, params, after):
        self.before = before
        self.opcode = opcode
        self.params = params
        self.after = after

    def __repr__(self):
        return (
            f"State({self.before}, {self.opcode}, {self.params}, {self.after})"
        )


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


def load_program(filename="day_16.txt"):
    with open(filename) as input_file:
        lines = input_file.read()
        instructions = []
        for program_line in lines.partition("\n\n\n\n")[2].splitlines():
            instructions.append(tuple(map(int, program_line.split(" "))))
        return instructions


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

    states_by_ops = defaultdict(list)

    for state in states:
        for op in ops:
            REGISTERS = eval(state.before)
            op(*state.params)
            if REGISTERS == eval(state.after):
                states_by_ops[op].append(state)

    counts = {
        op: set(Counter(map(lambda state: state.opcode, states)))
        for op, states in states_by_ops.items()
    }
    function_by_opcode = {}

    at_least_one_left = lambda: any(counts.values())

    while at_least_one_left():
        for func, possible_opcodes in counts.items():
            if len(possible_opcodes) == 1:
                opcode = possible_opcodes.pop()
                function_by_opcode[opcode] = func
                for _, po in counts.items():
                    if opcode in po:
                        po.remove(opcode)

    instructions = load_program()
    for opcode, *params in instructions:
        function_by_opcode[opcode](*params)
    print(REGISTERS[0])
