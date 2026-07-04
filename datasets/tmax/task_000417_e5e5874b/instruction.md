You are an engineer tasked with setting up a build system and mathematical data pipeline from scratch.

A polyglot mathematical evaluation engine uses a C library for high-speed calculation. Unfortunately, the latest vendored version of this library is broken, and our database contains malformed expressions that crash the engine.

Your task is divided into three stages:

**Stage 1: Fix and Build the Vendored Package**
A mathematical expression engine is vendored at `/app/fast-calc-2.1.0`. It contains source files, a `.S` assembly file for fast math routines, and a `Makefile`. 
Currently, running `make` fails due to incorrect compiler flags and a missing math library link step. 
1. Fix the `Makefile` to correctly build the shared library `libfastcalc.so`.
2. Ensure the assembly file is correctly compiled and linked into the shared object. 

**Stage 2: Write a Sanitizer (Adversarial Defense)**
The library's parser is vulnerable to specific mathematical structures that cause stack overflows or crashes. Write a C program at `/home/user/sanitizer.c` that compiles to `/home/user/sanitizer`. 
The program must:
- Accept a single mathematical expression string as a command-line argument (e.g., `./sanitizer "3 + (4 * 2)"`).
- Output strictly `ACCEPT` or `REJECT` to stdout.
- **Reject** criteria:
  1. Deep recursion: Any expression with a parenthesis nesting depth greater than 5.
  2. Unsupported operators: The presence of the modulo `%` or bitwise operators `&`, `|`, `^`.
  3. Literal division by zero (e.g., `/ 0`, `/0.0`).
- **Accept** criteria: Any valid mathematical expression containing numbers, `+`, `-`, `*`, `/`, and parentheses up to depth 5 that does not violate the reject criteria.
- You do not need to link `libfastcalc.so` for the sanitizer, just implement the string analysis logic in minimal C.

**Stage 3: Schema Migration**
You are provided with a SQLite database at `/home/user/math_data.db`. It contains a single table:
`equations_v1 (id INTEGER PRIMARY KEY, expression TEXT)`

Create a Python, Bash, or C script to perform a schema migration. 
1. Create a new table `equations_v2 (id INTEGER PRIMARY KEY, expression TEXT, status TEXT)`.
2. Read all rows from `equations_v1`.
3. Pass each `expression` through your compiled `/home/user/sanitizer`.
4. Insert the row into `equations_v2`, setting the `status` column to either `VALID` (if ACCEPT) or `INVALID` (if REJECT).

Ensure all code compiles without errors and the database migration is complete.