You are a platform engineer maintaining a CI/CD pipeline for a custom hardware emulator. We have a new requirement to implement a minimal Virtual Machine (VM) in C++ that interprets a custom assembly language, along with an end-to-end (E2E) testing script to validate its behavior.

Your task is to implement the VM, write test cases, and create an orchestration script.

Step 1: Implement the VM (`/home/user/vm.cpp`)
Write a C++ program that takes a single file path as a command-line argument, reads the custom assembly instructions from it, and executes them.
The VM has two registers: `R0` and `R1`, both initialized to 0.
Supported instructions (one per line, space separated):
- `LOAD <reg> <val>`: Load integer `<val>` into `<reg>` (e.g., `LOAD R0 5`).
- `ADD <reg1> <reg2>`: Add the value of `<reg2>` to `<reg1>` and store in `<reg1>`.
- `SUB <reg1> <reg2>`: Subtract the value of `<reg2>` from `<reg1>` and store in `<reg1>`.
- `OUT <reg>`: Print the value of `<reg>` to standard output followed by a newline.

Execution Quota (Rate Limiting/Validation): 
To prevent infinite loops in the CI environment, the VM must strictly limit execution. If the VM attempts to execute an 11th instruction (meaning strictly more than 10 instructions), it must immediately halt, print "QUOTA_EXCEEDED" to standard error, and exit with status code 42. Otherwise, on successful completion of the file, it should exit with status 0.

Step 2: Create Test Files
Create two assembly files in `/home/user/`:
- `/home/user/test_success.asm`: A valid program that calculates `15` using at least one LOAD and one ADD instruction, and prints it using OUT. It must contain 10 or fewer instructions.
- `/home/user/test_limit.asm`: A program that intentionally contains 12 `LOAD R0 1` instructions.

Step 3: Create the E2E Orchestration Script (`/home/user/run_ci.sh`)
Write a bash script that:
1. Compiles `/home/user/vm.cpp` to an executable named `/home/user/vm` using `g++ -std=c++17`.
2. Runs the VM against `/home/user/test_success.asm`. Captures the stdout.
3. Runs the VM against `/home/user/test_limit.asm`. Captures the exit code.
4. Writes a summary log to `/home/user/ci_summary.txt` exactly in this format:
```
SUCCESS_TEST_OUTPUT: <stdout_from_test_success>
LIMIT_TEST_EXIT_CODE: <exit_code_from_test_limit>
```

Make sure the bash script is executable. Run the script yourself to verify everything works and `/home/user/ci_summary.txt` is generated correctly.