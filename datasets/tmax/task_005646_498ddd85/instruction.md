You are tasked with building a polyglot build system and a custom compiler for a domain-specific mathematical language called Math State Machine (MSM). You will act as an engineer setting up a full pipeline from scratch in the directory `/home/user/polymath`.

Here are the requirements for the project:

1. **Workspace Setup**:
   - Create the directory `/home/user/polymath` and initialize it as a new Git repository.

2. **The MSM Language & State Machine Parser**:
   - Create a file `/home/user/polymath/model.msm` with the exact following contents:
     ```text
     INPUT x y
     t1 = ADD x 5.0
     t2 = MUL t1 y
     t3 = SUB t2 x
     OUTPUT t3
     ```
   - Write a Python script `/home/user/polymath/parser.py` that implements a custom state machine parser to read any `.msm` file and compile it to C code.
   - The parser must transition through states (e.g., `EXPECT_INPUT`, `READ_STATEMENTS`, `EXPECT_OUTPUT`).
   - It should parse `INPUT`, extract variables, parse statements with `ADD/SUB/MUL/DIV`, generate a symbol table (custom data structure to track variables), and output a valid C file containing a function: `double evaluate(double x, double y)`.
   - Running `python3 parser.py model.msm model.c` should generate a C file (`/home/user/polymath/model.c`) that implements the mathematical operations logically defined in the `.msm` file.

3. **Build System & Linking**:
   - Create a `Makefile` in `/home/user/polymath` with a default `all` target.
   - The build process must first invoke `parser.py` to generate `model.c`.
   - Then, it must compile `model.c` into a shared library named `libmodel.so` using GCC (ensure you use `-fPIC` and `-shared`).

4. **Testing Code**:
   - Write a Python script `/home/user/polymath/test_model.py` that uses the `ctypes` module to load `./libmodel.so`.
   - It must call the compiled `evaluate` function with arguments `x = 3.0` and `y = 4.0`.
   - The script must write the precise floating-point result to `/home/user/polymath/result.txt` (just the number as a string, e.g., "15.0").

5. **CI/CD Pipeline Setup**:
   - Simulate a CI/CD pipeline step by creating a pre-commit hook at `/home/user/polymath/.git/hooks/pre-commit`.
   - The hook must be an executable bash script that simply runs `make` and then runs `python3 test_model.py`. If either command fails, the hook must exit with a non-zero status, preventing the commit.

Execute all necessary commands to create these files, run the build via `make`, execute the test, and verify the entire pipeline.