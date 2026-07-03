You are an engineer setting up a polyglot mathematical build system and interpreter from scratch. The system consists of three components: a C library for prime number generation, a Rust utility for prime factorization, and a Go-based interpreter that orchestrates them by parsing a custom mathematical Domain Specific Language (DSL).

The project is located at `/home/user/project/`.
However, the previous engineer left the system in a broken state. You need to fix the build issues, implement the missing Go parser/interpreter, and run the system.

Here are the requirements and the state of the project:

1. **C Component (`/home/user/project/libmath/`):**
   - Contains `prime.c` which calculates the Nth prime number and prints it to stdout.
   - The `Makefile` is broken. It has syntax errors (spaces instead of tabs) and fails to compile because it's missing the `-lm` flag required for the math library. 
   - Fix the `Makefile` so that running `make` successfully produces an executable named `prime`.

2. **Rust Component (`/home/user/project/rs_calc/`):**
   - Contains a Cargo project that calculates the number of distinct prime factors of a given integer and prints the count to stdout.
   - The code in `src/main.rs` has a Rust ownership/borrow checker error because it improperly attempts to return a reference to a local variable or drops a borrowed value prematurely.
   - Fix `src/main.rs` so that `cargo build --release` successfully compiles the `rs_calc` executable.

3. **Go Component (`/home/user/project/go_machine/`):**
   - Contains `main.go`. You need to implement a state machine and parser in Go to act as an interpreter for a mathematical DSL.
   - The Go program must parse a file called `/home/user/project/program.math` line-by-line.
   - The interpreter maintains a single integer accumulator (starts at 0).
   - Supported instructions:
     - `ADD <X>`: Add the integer `<X>` to the accumulator.
     - `MUL <X>`: Multiply the accumulator by the integer `<X>`.
     - `PRIME <N>`: Execute the C binary (`/home/user/project/libmath/prime <N>`), parse its stdout, and ADD the result to the accumulator.
     - `FACTORS <N>`: Execute the Rust binary (`/home/user/project/rs_calc/target/release/rs_calc <N>`), parse its stdout, and ADD the result to the accumulator.
   - After completely parsing and executing `program.math`, the Go program must write the final accumulator value (as a plain text integer) to `/home/user/project/result.txt`.

**Execution:**
Once you have fixed the C Makefile, fixed the Rust code, and written the Go interpreter, compile the C and Rust components. Then, run your Go program:
`cd /home/user/project/go_machine && go run main.go`

Your task is complete when `/home/user/project/result.txt` exists and contains the correct final calculated integer based on `program.math`.