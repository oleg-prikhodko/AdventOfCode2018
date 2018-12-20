from day_16 import ops


def load_program(filename="day_19.txt"):
    with open(filename) as input_file:
        lines = input_file.readlines()[1:]
        program = []
        for line in lines:
            op_name, *params = line.split(" ")
            program.append((op_name, *map(int, params)))
        return program


if __name__ == "__main__":
    REGISTERS = [1, 0, 0, 0, 0, 0]
    ops = {op.__name__: op for op in ops}
    bind_register = 4
    instruction_pointer = 0
    program = load_program("day_19.txt")
    timer = 0
    while instruction_pointer < len(program):
        opname, *params = program[instruction_pointer]
        REGISTERS[bind_register] = instruction_pointer
        ops[opname](REGISTERS, *params)
        instruction_pointer = REGISTERS[bind_register]
        instruction_pointer += 1

        if timer % 1000 == 0:
            print(REGISTERS)
        timer += 1
