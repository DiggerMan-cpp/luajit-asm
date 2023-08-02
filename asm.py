import sys

def disassemble_bytecode(bytecode):
    opcodes = [
        'MOVE', 'LOADK', 'LOADKX', 'LOADBOOL', 'LOADNIL', 'GETUPVAL', 'GETTABUP', 'GETTABLE', 'SETTABUP', 'SETUPVAL',
        'SETTABLE', 'NEWTABLE', 'SELF', 'ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'POW', 'UNM', 'NOT', 'LEN', 'CONCAT',
        'JMP', 'EQ', 'LT', 'LE', 'TEST', 'TESTSET', 'CALL', 'TAILCALL', 'RETURN', 'FORLOOP', 'FORPREP', 'TFORCALL',
        'TFORLOOP', 'SETLIST', 'CLOSURE', 'VARARG', 'EXTRAARG'
    ]

    instructions = []
    data = []
    i = 0
    while i < len(bytecode):
        opcode = bytecode[i]
        if opcode < len(opcodes):
            instr = opcodes[opcode]
            if instr in ['MOVE', 'LOADK', 'LOADBOOL', 'GETUPVAL', 'GETTABUP', 'GETTABLE', 'SETTABUP', 'SETUPVAL', 'SETTABLE', 'NEWTABLE', 'SELF', 'ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'POW', 'UNM', 'NOT', 'LEN', 'CONCAT', 'JMP', 'EQ', 'LT', 'LE', 'TEST', 'TESTSET', 'CALL', 'TAILCALL', 'RETURN', 'FORLOOP', 'FORPREP', 'TFORCALL', 'TFORLOOP', 'SETLIST', 'CLOSURE', 'VARARG']:
                arg = bytecode[i + 1]
                if instr == 'LOADK' and arg >= 0xFF:
                    instr = 'LOADKX'
                    arg = (bytecode[i + 1] << 8) | bytecode[i + 2]
                    i += 2
                if instr in ['LOADK', 'GETTABUP']:
                    try:
                        hex_data = ''.join(f'{byte:02X}' for byte in bytecode[arg + 1: arg + 1 + bytecode[arg]])
                        str_data = bytes.fromhex(hex_data).decode('utf-8')
                    except (ValueError, UnicodeDecodeError):
                        str_data = "InvalidString"
                    arg = f'"{str_data}"'
                instr += " " + str(arg)
                i += 1

            instructions.append((i, instr))
        else:
            length = bytecode[i + 1]
            if i + 2 + length <= len(bytecode): 
                str_data = ""
                valid_ascii = True
                for j in range(i + 2, i + 2 + length):
                    if 32 <= bytecode[j] <= 126:
                        str_data += chr(bytecode[j])
                    else:
                        valid_ascii = False
                        str_data += f'.{bytecode[j]:02X}'
                if valid_ascii:
                    instructions.append((i, str_data))
                else:
                    instructions.append((i, ' ')) # UNKNOWN_OPCODE_STRING
                    data.append(f'_str{i}: .byte {str_data}')
            else:
                instructions.append((i, ' ')) # UNKNOWN_OPCODE_STRING
                data.append(f'_str{i}: .byte {" ".join(f"{byte:02X}" for byte in bytecode[i + 2: i + 2 + length])}')

            i += 1 + length

        i += 1

    return instructions, data

def save_assembly_code(bytecode, output_file):
    instructions, data = disassemble_bytecode(bytecode)
    with open(output_file, 'w') as file:
        file.write("; luajit bytecode -> asm, by Digger Man\n\n")

        if data:
            file.write(".data\n")
            for str_data in data:
                file.write(f'{str_data}\n')

        file.write("\n.text\n")
        for instr in instructions:
            file.write(f"{instr[0]:04X}: {instr[1]}\n")

if len(sys.argv) < 2:
    print("Usage: python asm.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = input_file + ".asm"

with open(input_file, "rb") as file:
    bytecode = file.read()

save_assembly_code(bytecode, output_file)
