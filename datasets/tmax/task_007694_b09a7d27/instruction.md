I was trying to write a Rust utility to perform a specific numerical algorithm (calculating the maximum number of Collatz conjecture steps for any integer up to a given limit `N`), but I keep hitting Rust borrow checker errors and ownership issues. I've decided to pivot and just write this utility in Python instead.

Your task is to:
1. Read the broken Rust source file located at `/home/user/calc.rs`. Understand the numerical algorithm it is attempting to perform.
2. Translate this logic into a Python script at `/home/user/calc.py`.
3. Set up dependency management: create a `/home/user/requirements.txt` file that includes `pydantic`.
4. Implement input validation in your Python script using `pydantic`. The script should accept a single integer argument `N` from the command line (e.g., `python /home/user/calc.py 50`). 
5. Use a Pydantic model to validate that `N` is an integer and that `1 <= N <= 5000`. If `N` is outside this range or invalid, print exactly `Validation Error` to standard output and exit with code 1.
6. If the input is valid, calculate the result (the maximum Collatz steps for any starting number from 1 up to and including `N`) and write the integer result to `/home/user/output.txt`.

For example, if the script is run as `python /home/user/calc.py 10`, it should calculate the Collatz steps for 1 through 10, find the maximum number of steps, and write just that maximum integer to `/home/user/output.txt`.

Ensure your Python script is executable and correctly implements the algorithm intended by the broken Rust code.