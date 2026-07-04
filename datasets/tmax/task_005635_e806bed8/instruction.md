You are an open-source maintainer reviewing a pull request for a custom Assembly Virtual Machine in Python. The PR is broken and needs to be fixed before merging.

The repository is located at `/home/user/repo`.

The PR introduces two files:
1. `/home/user/repo/assembler.py`: A state machine parser that executes a minimal assembly language. The PR author mentioned there might be a bug in the `JNZ` (Jump if Not Zero) instruction logic where it doesn't correctly update the Program Counter (`self.pc`).
2. `/home/user/repo/test_assembler.py`: A test suite using `unittest`. The test `test_basic_addition` uses `unittest.mock.patch` to mock `sys.stdout`, but the test is failing with a `TypeError` due to an incorrect mock setup.

Your tasks:
1. Debug and fix the bug in `assembler.py` so that the `JNZ` instruction jumps to the absolute line index provided as its argument, instead of doing a relative jump. (Line indices are 0-based).
2. Fix the broken mock setup in `test_assembler.py` so that `pytest /home/user/repo/test_assembler.py` passes successfully.
3. Perform assembly-level analysis by writing a minimal program in this custom assembly language. Save it to `/home/user/repo/program.asm`. The program must calculate the sum of integers from 5 down to 1 (i.e., 5 + 4 + 3 + 2 + 1 = 15). 
   - The final result (15) must be the only value left on the top of the stack when the program finishes executing.
   - The VM supports `PUSH <val>`, `POP`, `ADD`, `SUB` (pops A, pops B, pushes B-A), `STORE <var>`, `LOAD <var>`, `JMP <line>`, and `JNZ <line>`.
   - Empty lines and lines starting with `#` are skipped but still count towards the line index.

To verify your work, make sure all tests pass and that running the VM on your `program.asm` leaves `15` at the top of the stack.