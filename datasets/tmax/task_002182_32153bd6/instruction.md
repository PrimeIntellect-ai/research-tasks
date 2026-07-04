You are a build engineer managing artifacts for a legacy mathematical computation engine written in C. The project is located in `/app/math_engine` and is built using CMake. Currently, the project is broken due to linkage issues and incomplete source files. 

Your task is to fix the project, complete the implementation, and ensure it correctly builds and runs.

Here are the requirements:

1. **Audio Specification Extract:**
   There is an audio file at `/app/operator_spec.wav`. This file contains an engineering note recorded by the original architect. You need to transcribe this audio to find the mathematical definition of a custom operator denoted by the `@` symbol. You must implement this operator in the expression parsing and evaluation engine located in `/app/math_engine/src/eval.c`. 

2. **CMake and Linkage Fix:**
   The project consists of a shared library (`libmathast.so`) and a CLI tool (`eval_tool`). Currently, the `CMakeLists.txt` is configured incorrectly. It either fails to find the shared library at link time or produces an executable that fails to run because it cannot locate `libmathast.so` at runtime. Modify `/app/math_engine/CMakeLists.txt` to correctly link the shared library to `eval_tool` and embed the correct RPATH so that `eval_tool` runs standalone without needing `LD_LIBRARY_PATH`.

3. **AST Serialization:**
   The engine uses an Abstract Syntax Tree (AST) to evaluate expressions. You must implement the missing binary serialization and deserialization routines in `/app/math_engine/src/serialize.c`. The `eval_tool` workflow operates as follows:
   - Parse the mathematical string into an AST.
   - Serialize the AST into a binary buffer.
   - Deserialize the binary buffer back into an AST.
   - Evaluate the deserialized AST and print the result as a single integer to stdout.

4. **Expected Output:**
   The `eval_tool` executable must take exactly one argument: the mathematical expression string. 
   It should output strictly the integer result of the evaluated expression followed by a newline. No extra text, debugging info, or hex dumps. 
   Supported operators are `+`, `-`, `*`, and the custom `@` operator (defined in the audio file). Standard operator precedence applies, with `@` having the same precedence as `*`. All numbers will be integers, and calculations should be done using 64-bit signed integers.

Fix the build, implement the logic, and compile the executable at `/app/math_engine/build/eval_tool`.