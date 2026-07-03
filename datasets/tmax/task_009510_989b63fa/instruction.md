You are a developer tasked with fixing a broken C project that currently fails to build due to a circular dependency, simulating a real-world scenario where modularity has gone wrong. The project is located in `/home/user/project`.

The project contains the following source files:
- `a.c` and `a.h` (contains `func_a`)
- `b.c` and `b.h` (contains `func_b`)
- `main.c` (the entry point)

Currently, `func_a` calls `func_b`, and `func_b` calls `func_a`. 
A colleague has provided a patch file `/home/user/project/fix.patch` that fixes the logic in `b.c` to break the circular dependency. However, they saved the patch file with the wrong character encoding (it is encoded in UTF-16LE instead of UTF-8), so standard tools are rejecting it.

Your task is to write a self-contained Bash build script at `/home/user/build.sh` that performs the following steps when executed:
1. Fixes the character encoding of the patch file (converts it to UTF-8).
2. Applies the fixed patch to the source code to break the circular dependency.
3. Compiles `a.c` into a shared library named `liba.so`.
4. Compiles `b.c` into a shared library named `libb.so`.
5. Compiles `main.c` and links it against `liba.so` and `libb.so` to produce an executable named `main` inside `/home/user/project`.
6. Configures the linking (using rpath) so that the `main` executable can find the shared libraries in its current directory (`/home/user/project`) at runtime, WITHOUT needing to export `LD_LIBRARY_PATH` before running it.

Requirements:
- Ensure your script `/home/user/build.sh` is executable.
- The compiled executable must be located at `/home/user/project/main`.
- We will verify your task by running `/home/user/project/main` directly in a clean shell environment. It must execute successfully and output the calculated result.