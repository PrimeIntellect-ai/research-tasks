You are a systems programmer debugging a C library linking issue. 

You have been given a compiled shared library `/home/user/libmath.so` and a C program `/home/user/main.c`. 
The shared library was originally written in C++ and compiled without `extern "C"`. Because of this, its exported function `int calculate(int a, int b)` has a mangled symbol name. 

The C program `/home/user/main.c` attempts to call `calculate` directly:
```c
#include <stdio.h>

int calculate(int a, int b);

int main() {
    printf("Result: %d\n", calculate(5, 3));
    return 0;
}
```
Currently, if you try to compile `main.c` against `libmath.so`, it fails with an `undefined reference to 'calculate'` linker error.

Your task is to automate the discovery and resolution of this ABI mismatch by writing an end-to-end Python orchestration script at `/home/user/fix_link.py`.

The script `/home/user/fix_link.py` must perform the following steps when executed:
1. Run a shell command (like `nm`) on `/home/user/libmath.so` and parse its output programmatically to find the mangled C++ symbol name for the `calculate` function (it will have a signature taking two integers).
2. Generate a minimal x86_64 GNU assembly file at `/home/user/bridge.s`. This assembly file must define a global C-compatible symbol `calculate` that simply acts as a trampoline (e.g., using a `jmp` instruction) to the mangled C++ function.
3. Compile an executable at `/home/user/app` by compiling `/home/user/main.c` and `/home/user/bridge.s` together, linking against `/home/user/libmath.so`. Ensure the library search path (`rpath`) is configured so the binary can find the shared object in `/home/user` at runtime.
4. Execute `/home/user/app` and write its standard output to a log file exactly at `/home/user/test_output.log`.

Requirements:
- Do not modify `/home/user/main.c`.
- Do not recompile or attempt to modify `/home/user/libmath.so` (you do not have the source code).
- `/home/user/fix_link.py` must handle the entire process without manual intervention.
- The generated `/home/user/bridge.s` must be valid x86_64 assembly.

Run your Python script to complete the task and generate the executable and log file.