You are an open-source maintainer reviewing a Pull Request for a data processing library, located in `/home/user/pr-review`. The PR adds a C-based Virtual Machine (VM) to process binary data streams quickly, with a Python ctypes wrapper. 

However, the contributor left the PR in a broken state. Your task is to fix the build system, debug the C emulator, fix the Python tests, and finally use the VM to process a dataset.

Here are the requirements:

1. **Fix the Makefile:** The `Makefile` in `/home/user/pr-review` is supposed to compile `vm.c` into a shared library named `libvm.so`. It is currently failing or producing invalid binaries because it is missing the necessary compiler flags for building a shared library (e.g., Position Independent Code). Fix the `Makefile`.

2. **Debug the C Emulator:** The file `vm.c` implements a simple stack-based VM. The unit tests are failing because one of the basic arithmetic instructions in `vm.c` has a logical bug. Find the bug in the C code and fix it.

3. **Fix the Python Tests:** The file `test_vm.py` contains unit tests for the C extension. The `ctypes` bindings have a typo in the argument types for the C function `execute_vm`, causing memory corruption or type errors. Fix `test_vm.py` so that `pytest test_vm.py` passes successfully.

4. **Write Assembly / Bytecode:** The file `process.py` is incomplete. It needs to read `/home/user/pr-review/input.bin`, process it using the VM, and write the results to `/home/user/pr-review/output.json` (as a JSON list of integers). 
   You must implement the `BYTECODE` variable in `process.py`. The VM executes the bytecode once for *each* byte in the input array. 
   You need to write bytecode that applies the mathematical function `y = (2 * x) + 7` (where x is the input byte) and writes it to the output.

   **VM Instruction Set Architecture:**
   - `0x01 <val>`: PUSH (pushes the 1-byte `<val>` onto the stack)
   - `0x02`: ADD (pops A, pops B, pushes B + A)
   - `0x03`: SUB (pops A, pops B, pushes B - A)
   - `0x04`: MUL (pops A, pops B, pushes B * A)
   - `0x05`: LOAD_INPUT (pushes the current input byte onto the stack)
   - `0x06`: STORE_OUTPUT (pops A, writes A to the current output position)
   - `0x07`: HALT (ends execution for the current byte, moves to the next input byte)

Once you have fixed the files, run `python process.py`. The success of this task will be verified by checking that `libvm.so` compiles, the tests pass, and `/home/user/pr-review/output.json` contains the correctly processed data.