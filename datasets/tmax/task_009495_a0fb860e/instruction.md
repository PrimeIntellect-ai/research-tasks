You are tasked with fixing a buggy C-based mathematical virtual machine (VM) and verifying its correctness against a pure Python reference implementation using property-based testing. 

You have been provided with a directory at `/home/user/math_vm` containing:
1. `vm.c`: A C library implementing a simple stack-based VM for evaluating postfix mathematical expressions (Opcodes: 0=PUSH, 1=ADD, 2=SUB, 3=MUL). It currently has critical memory safety issues (buffer overflows and memory leaks).
2. `pyvm.py`: A Python wrapper that uses `ctypes` to interface with `libvm.so`, alongside a pure Python reference implementation of the same VM.
3. `Makefile`: A makefile to build `libvm.so`.

**Your objectives:**
1. **Repair the C Emulator (`vm.c`):** Fix the memory leaks and buffer overflow vulnerabilities in `vm.c`. The VM must safely handle an arbitrary number of instructions without crashing, bounds-checking correctly, and leaking zero memory. Ensure you do not change the function signature of `execute_vm`.
2. **Rebuild the library:** Use `make` to compile the repaired C extension into `libvm.so`.
3. **Implement Property-Based Testing (`test_vm.py`):** 
   - Create a Python script at `/home/user/math_vm/test_vm.py`.
   - Use the `hypothesis` library (`pip install hypothesis`) to write a property-based test.
   - The test must generate random valid or invalid instruction sequences (lists of tuples `(opcode, value)` where `opcode` is 0-3 and `value` is between -1000 and 1000).
   - For each sequence, run both `pyvm.execute_py` and `pyvm.execute_c`. 
   - Catch `ValueError` (which indicates a stack underflow/invalid expression). If `execute_py` raises a `ValueError`, `execute_c` must also raise a `ValueError`. If `execute_py` succeeds, `execute_c` must succeed and return the exact same integer result.
   - Run the property tests. If the tests pass without falsification, the script must write the exact string `PROPERTY_TESTS_PASSED` to a log file at `/home/user/math_vm/test_success.log`.

Your final verification is the existence and correct content of `/home/user/math_vm/test_success.log` produced by a passing property-based test script, alongside a correctly patched `vm.c` that compiles and runs without leaks.