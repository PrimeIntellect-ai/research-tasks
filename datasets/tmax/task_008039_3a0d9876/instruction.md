You have recently inherited an unfamiliar codebase. Among the utilities is a numerical solver written in C, located at `/home/user/newton_root.c`. This program uses the Newton-Raphson method to find a root of the function f(x) = x^3 - 2x + 2. It takes a single double-precision float as a command-line argument representing the initial guess.

Users have reported a forensics issue: for certain specific initial guesses, the program completely hangs, consuming 100% CPU without ever producing an output. This is a classic convergence failure.

Your task:
1. Understand the provided C code and identify the cause of the convergence failure.
2. Use a fuzz testing approach (e.g., writing a short script to test various inputs) to find an integer input between -5 and 5 that triggers this infinite loop / oscillation. 
3. Write the integer value that causes the hang to `/home/user/failing_input.txt`.
4. Repair the convergence failure in the codebase. Modify the C code so that it keeps track of the number of iterations.
5. Add assertion-based intermediate validation: if the number of iterations reaches 100, the program should print `Convergence failed\n` and exit with status code 1.
6. Save your fixed C code to `/home/user/fixed_newton_root.c` and compile it into an executable named `/home/user/fixed_newton_root`.

Ensure that:
- `/home/user/failing_input.txt` contains only the failing integer starting guess.
- Your fixed executable correctly finds the root for valid inputs (like `2.0`), exiting with 0.
- Your fixed executable correctly catches the convergence failure for the failing input, prints "Convergence failed", and exits with 1.