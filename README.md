# luajit-asm
luajit bytecode -> pseudo asm
# for python 
Usage python asm.py name.luac

# for c++ build
g++ main.cpp

# for c++ usage
./file.exe name.luac
# difference
The C++ version keeps .data and .text in the same place, while the python version separates .data and .text, but the c++ version does not store instruction arguments, which is why you should use both the python version and the c++ version for a better understanding of the code
