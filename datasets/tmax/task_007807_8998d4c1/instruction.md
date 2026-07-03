I am migrating a legacy numerical processing system from Python 2 to Python 3. The system consists of a Python script that compiles a custom mathematical assembly language into a proprietary bytecode, and a C-based Virtual Machine (VM) that executes it. 

I successfully ported the Python compiler to Python 3 and compiled a new mathematical routine, saving the bytecode to `/home/user/prog.bin`. However, I accidentally lost the C source code for the VM emulator!

I need you to write a new C interpreter for this bytecode from scratch and execute the program.

Here is the specification for the VM and bytecode:
- **Registers**: 4 registers (`R0`, `R1`, `R2`, `R3`), each holding a 32-bit signed integer. All initialized to 0.
- **Program Counter (PC)**: Starts at 0 (0-indexed by instruction, not by byte).
- **Instruction Format**: 32-bit fixed-length instructions (Little Endian).
  - Byte 0: Opcode
  - Byte 1: Arg1 (Usually destination register index)
  - Byte 2: Arg2 (Source register 1 index)
  - Byte 3: Arg3 (Source register 2 index, or immediate value)

**Opcodes**:
- `0x01`: `LOAD_IMM` - `R[Arg1] = (int8_t)Arg3` (Sign-extended)
- `0x02`: `ADD` - `R[Arg1] = R[Arg2] + R[Arg3]`
- `0x03`: `SUB` - `R[Arg1] = R[Arg2] - R[Arg3]`
- `0x04`: `MUL` - `R[Arg1] = R[Arg2] * R[Arg3]`
- `0x05`: `DIV` - `R[Arg1] = R[Arg2] / R[Arg3]` (Assume no division by zero)
- `0x06`: `JZ` - Jump if Zero: If `R[Arg1] == 0`, jump the PC by `(int8_t)Arg3` instructions. (Offset is relative to the *next* instruction that would have executed).
- `0x07`: `JMP` - Jump the PC unconditionally by `(int8_t)Arg3` instructions. (Relative to the *next* instruction).
- `0x08`: `PRINT` - Append the integer value of `R[Arg1]` as a string followed by a newline (`\n`) to `/home/user/vm_output.txt`.
- `0x09`: `HALT` - Stop execution cleanly.

**Requirements**:
1. Write the VM in C. Save the source to `/home/user/vm.c`.
2. Compile it using GCC (e.g., `gcc -o /home/user/vm /home/user/vm.c`).
3. Your compiled VM must accept the binary file path as its first command-line argument (e.g., `./vm /home/user/prog.bin`).
4. Read the instructions from the binary into memory (assume maximum 1024 instructions).
5. Execute the instructions in a loop until a `HALT` instruction is reached.
6. Once built, run `/home/user/prog.bin` using your VM.

Ensure the final output is correctly written to `/home/user/vm_output.txt`.