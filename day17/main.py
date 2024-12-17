from pathlib import Path

def load_program():
    text = Path("input.txt").read_text()
    registers = [int(line.split(": ")[1]) for line in text.splitlines()[:3]]
    program = [int(x) for x in text.splitlines()[-1][9:].split(",")]
    return registers, program


def step(registers, program, pointer, output):
    opcode, operand = program[pointer:pointer+2]
    pointer += 2
    
    match opcode:
        case 0 | 6 | 7:  # Division operations
            val = int(registers[0] / (2 ** combo(operand, registers)))
            registers[{0:0, 6:1, 7:2}[opcode]] = val
        case 1:  # XOR with literal
            registers[1] ^= operand
        case 2:  # Set B from combo mod 8
            registers[1] = combo(operand, registers) % 8
        case 3:  # Conditional jump
            pointer = operand if registers[0] != 0 else pointer
        case 4:  # XOR B with C
            registers[1] ^= registers[2]
        case 5:  # Output
            output.append(combo(operand, registers) % 8)
        case _:
            raise ValueError(f"Unknown opcode: {opcode}")

    return registers, pointer, output


def combo(operand, registers):
    return operand if operand <= 3 else registers[operand - 4]


def run(registers, program):
    pointer, output = 0, []
    while pointer < len(program):
        registers, pointer, output = step(registers, program, pointer, output)

    return registers, output

    

print("Part 1:", ",".join(map(str,run(*load_program())[1])))
