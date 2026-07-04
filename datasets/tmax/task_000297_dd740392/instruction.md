You have been given a broken C project in `/home/user/vm_project` that implements a simple stack-based virtual machine (VM). The project currently fails to compile due to some missing includes and strict compiler flags, and it also contains severe memory safety issues (buffer overflows and underflows) that cause undefined behavior when executing malformed programs.

Your goal is to fix the project, resolve the memory safety issues, and build an end-to-end test orchestrator.

Here is what you need to do:

1. **Fix Compilation:** Fix the C source code in `/home/user/vm_project/src/` so that running `make` in `/home/user/vm_project` successfully builds the `simple_vm` executable without any warnings or errors. Do not modify the `Makefile`.

2. **Fix Memory Safety:** The VM has a fixed stack size of 10 (`MAX_STACK = 10`). 
   - If a `PUSH` operation exceeds this limit, the VM must print exactly `Error: Stack Overflow` to standard output and immediately exit with status code `1`.
   - If a `POP`, `ADD`, or `PRINT` operation tries to read from an empty stack (or a stack with insufficient items for the operation), it must print exactly `Error: Stack Underflow` to standard output and exit with status code `1`.

3. **Implement End-to-End Testing:** Write a Python script `/home/user/vm_project/test_runner.py` that orchestrates the testing of the `simple_vm` executable. 
   - The script should look for all `.asm` files in `/home/user/vm_project/tests/`.
   - For each `.asm` file, run `./simple_vm tests/<filename>`.
   - Compare the standard output and exit code of the VM to the expected output found in the corresponding `.expected` file in the `tests/` directory. (If an error message is expected, the `.expected` file will contain it, and the expected exit code is `1`. Otherwise, the expected exit code is `0`).
   - The Python script must generate a JSON report at `/home/user/vm_project/report.json` with the following structure:
     ```json
     {
       "valid_program.asm": "pass",
       "overflow_program.asm": "pass",
       "failing_test.asm": "fail"
     }
     ```
   - "pass" means the output and exit code exactly matched the expectations. "fail" means they did not.

To complete the task, leave the fixed C source code, the compiled executable, the `test_runner.py` script, and the generated `report.json` in `/home/user/vm_project`.