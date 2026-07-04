You are a script developer creating a fast, cross-platform utility to parse a custom text protocol. The protocol embeds commands in a noisy text stream. To maximize performance on your primary servers, the core calculation function must be written in x86_64 assembly, while ARM servers will use a standard C++ fallback.

Your task is to build this utility by combining C++, x86_64 Assembly, a custom state machine parser, and a polyglot Makefile for cross-compilation.

**Requirements:**

1. **State Machine Parser (`parser.cpp`)**:
   - Write a C++ program that reads a file path from the first command-line argument.
   - Implement a strict finite state machine (FSM) that reads the file byte-by-byte to extract commands formatted exactly as: `[CMD: <action>]`
   - Note: There is exactly one space after the colon. `<action>` consists of lowercase/uppercase letters only.
   - Any character sequence not matching this exact structure should be ignored as noise.
   - For every extracted `<action>`, call an external C-linkage function: `extern "C" int process_action(const char* action, int len);`
   - Print the result to standard output in the format: `<action>:<result>` (one per line).

2. **Assembly Implementation (`action_x86.s`)**:
   - Write a minimal x86_64 assembly file that implements `process_action`.
   - The function must iterate over the string and return the sum of the ASCII values of the characters in the `action` string.

3. **C++ Fallback (`action_arm.cpp`)**:
   - Write a C++ implementation of `process_action` with the exact same logic (returning the ASCII sum), to be used when cross-compiling for ARM.

4. **Polyglot Build Orchestration (`Makefile`)**:
   - Create a `Makefile` in `/home/user/workspace` with two targets: `x86` (default) and `arm`.
   - `make x86` must compile `parser.cpp` and `action_x86.s` using `g++` into an executable named `sys_parser`.
   - `make arm` must cross-compile `parser.cpp` and `action_arm.cpp` using `aarch64-linux-gnu-g++` into an executable named `sys_parser_arm`.

**Execution:**
- The input file is located at `/home/user/input.txt`.
- Set up your files in `/home/user/workspace`.
- Run `make x86` and `make arm`.
- Execute `./sys_parser /home/user/input.txt` and redirect the standard output to `/home/user/parser_output.txt`.

Ensure your Makefile correctly handles the compilation flags and your state machine correctly recovers from partial matches (e.g., `[CMD: [CMD: run]`).