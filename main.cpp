#include <iostream>
#include <fstream>
#include <iomanip>
#include <vector>

std::vector<std::string> opcodes = {
    "MOVE", "LOADK", "LOADKX", "LOADBOOL", "LOADNIL", "GETUPVAL", "GETTABUP", "GETTABLE", "SETTABUP", "SETUPVAL",
    "SETTABLE", "NEWTABLE", "SELF", "ADD", "SUB", "MUL", "DIV", "MOD", "POW", "UNM", "NOT", "LEN", "CONCAT",
    "JMP", "EQ", "LT", "LE", "TEST", "TESTSET", "CALL", "TAILCALL", "RETURN", "FORLOOP", "FORPREP", "TFORCALL",
    "TFORLOOP", "SETLIST", "CLOSURE", "VARARG", "EXTRAARG"
};

void disassembleBytecode(const std::vector<uint8_t>& bytecode, std::ofstream& outputFile) {
    std::string instruction;
    size_t index = 0;
    while (index < bytecode.size()) {
        uint8_t opcode = bytecode[index];
        if (opcode < opcodes.size()) {
            instruction = opcodes[opcode];
            if (opcode == 1) {
                uint8_t arg = bytecode[index + 1];
                if (arg >= 0xFF) {
                    instruction = "LOADKX";
                    arg = (bytecode[index + 1] << 8) | bytecode[index + 2];
                    index += 2;
                }
                if (instruction == "LOADK" || instruction == "GETTABUP") {
                    std::string strData;
                    try {
                        for (int i = 0; i < arg; ++i) {
                            uint8_t byte = bytecode[index + i + 1];
                            strData += static_cast<char>(byte);
                        }
                    } catch (const std::exception& e) {
                        strData = "InvalidString";
                    }
                    instruction += " \"" + strData + "\"";
                } else {
                    instruction += " " + std::to_string(arg);
                }
                index++;
            }
        } else {
            size_t length = bytecode[index + 1];
            instruction = "UNKNOWN_OPCODE";
            std::string strData;
            for (int i = 0; i < length; ++i) {
                uint8_t byte = bytecode[index + i + 2];
              strData += byte < 32 || byte > 126 ? "." : std::string(1, static_cast<char>(byte));
            }
            instruction += " " + strData;
            index += length;
        }
        outputFile << std::hex << std::setw(4) << std::setfill('0') << index << ": " << instruction << std::endl;
        index++;
    }
}

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cout << "Usage: ./asm.exe <input_file>" << std::endl;
        return 1;
    }

    std::string input_file = argv[1];
    std::ifstream inputFileStream(input_file, std::ios::binary);
    if (!inputFileStream) {
        std::cerr << "Error opening input file" << std::endl;
        return 1;
    }

    std::vector<uint8_t> bytecode(std::istreambuf_iterator<char>(inputFileStream), {});
    std::string output_file = input_file + ".asm";
    std::ofstream outputFileStream(output_file);
    if (!outputFileStream) {
        std::cerr << "Error creating output file" << std::endl;
        return 1;
    }

    disassembleBytecode(bytecode, outputFileStream);

    return 0;
}
