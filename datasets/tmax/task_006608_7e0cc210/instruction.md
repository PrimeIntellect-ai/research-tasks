You are helping a developer organize and fix a mixed-language project. The project consists of a C program that delegates mathematical operations to an Assembly shared library. The build process was lost, and the developer needs you to recreate the shared library, compile the project, and successfully link it.

Here is the current state of the project directory at `/home/user/project/`:
- `src/main.c`: A C program that takes two integer command-line arguments, calls an external function `int do_math(int a, int b);`, and prints the result.
- `config.json`: A JSON file specifying the mathematical operation the project is currently configured for. It has the format `{"operation": "<op>"}`, where `<op>` can be "add", "sub", or "mul".
- `lib/`: An empty directory intended for shared libraries.
- `bin/`: An empty directory intended for the final executable.

Your task:
1. Parse `/home/user/project/config.json` to determine the required operation.
2. Write a minimal x86_64 assembly file (use AT&T or Intel syntax, compatible with GCC/GNU Assembler) that implements the `do_math` function according to the operation specified in the JSON (e.g., if it says "sub", `do_math` should return `a - b`).
3. Compile your assembly file into a shared library named `libmath.so` and place it in `/home/user/project/lib/`.
4. Compile `/home/user/project/src/main.c` into an executable named `app` and place it in `/home/user/project/bin/`. You must link it against the `libmath.so` library. Ensure the executable can find the shared library at runtime without relying on global environment variables like `LD_LIBRARY_PATH` (hint: use rpath).
5. Test your program by running `/home/user/project/bin/app 50 15` and redirect the standard output to `/home/user/project/output.txt`.

Ensure all files are placed exactly in their designated directories.