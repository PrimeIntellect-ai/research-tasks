You are an engineer tasked with setting up a polyglot mathematical build system from scratch. Your team has inherited a legacy pipeline that generates prime numbers in C and computes their Collatz conjecture stopping times in Ruby. Your goal is to repair the C build process, port the Ruby logic to Python, and write an end-to-end Python orchestrator to automate the CI/CD test phase.

The workspace is located at `/home/user/polyglot_math`. Inside, you will find:
- `generate_primes.c`: A C program that takes a single integer `N` as a command-line argument and prints all prime numbers up to `N` (inclusive), one per line. It uses the `sqrt` function from `math.h`.
- `Makefile`: A broken Makefile for the C program.
- `collatz.rb`: A Ruby script that reads integers from `stdin` (one per line) and prints `number,collatz_steps` to `stdout`.
- `expected_output.txt`: The canonical, correctly sorted output for `N = 100`.

Your tasks are to:
1. **Repair the Makefile**: Modify `/home/user/polyglot_math/Makefile` so that running `make` correctly compiles `generate_primes.c` into an executable named `generate_primes`. Fix any syntax errors (e.g., tabs/spaces) and ensure proper linking for the math library.
2. **Translate Code**: Translate `collatz.rb` into Python. Create `/home/user/polyglot_math/collatz.py` which must do exactly what the Ruby script did: read integers from standard input and print `number,collatz_steps`.
3. **Build the CI/CD Orchestrator**: Create a Python script at `/home/user/polyglot_math/pipeline.py` that automates the following end-to-end pipeline:
   - Executes `make clean` followed by `make`.
   - Executes `./generate_primes 100`.
   - Feeds the generated primes via standard input into `python3 collatz.py`.
   - Parses the output (`number,collatz_steps`) and sorts the results. The sorting must be **numeric, ascending**, primarily by `collatz_steps`, and secondarily by `number`.
   - Writes the sorted results to `/home/user/polyglot_math/pipeline_output.txt`.
   - Programmatically diffs the contents of `/home/user/polyglot_math/pipeline_output.txt` against `/home/user/polyglot_math/expected_output.txt`.
   - If the contents match perfectly, the script should print `PIPELINE SUCCESS` to standard output and exit with code `0`. If they do not match, it must print `PIPELINE FAILED` and exit with code `1`.

All files must be created or modified directly in `/home/user/polyglot_math`.