I need you to set up a minimal polyglot build system and write a small emulator for a custom "Stack Machine" language. You can write the emulator itself in any language you prefer (Python, C, Node.js, Bash, etc.), but you must provide standard shell scripts to build, run, and test it.

**The Stack Machine Language (SML):**
The language processes instructions line-by-line. It maintains a single stack of integers.
Supported instructions:
* `PUSH <int>`: Pushes an integer onto the stack.
* `ADD`: Pops the top two values, adds them, and pushes the result.
* `SUB`: Pops the top two values, subtracts the top value from the second-to-top value, and pushes the result. (e.g., if stack is [bottom: 10, top: 3], SUB leaves 7).
* `PRINT`: Pops the top value and prints it to standard output on a new line.

If an instruction like `ADD`, `SUB`, or `PRINT` is called when there are insufficient items on the stack, the emulator should print `ERROR` to standard output and immediately exit.

**Your Objectives:**

1. **Write the Emulator**: Implement the SML emulator in your language of choice.
2. **`build.sh`**: Create an executable script `/home/user/build.sh`. This script should contain any setup, compilation, or dependency installation your emulator needs (e.g., `gcc emulator.c -o emulator`, or just `chmod +x emulator.py`).
3. **`run_interpreter.sh`**: Create an executable script `/home/user/run_interpreter.sh`. It must take exactly one argument: the path to an SML file. It should execute your emulator on that file.
   Usage example: `./run_interpreter.sh /home/user/tests/test1.sm`
4. **`test.sh`**: Create an executable script `/home/user/test.sh`. This script is an integration test runner. It must:
   - Find all `.sm` files in the `/home/user/tests/` directory (which already exists).
   - Run `run_interpreter.sh` on each file.
   - Collect all the standard outputs from these runs.
   - Sort the output lines numerically in ascending order.
   - Save the final sorted output to `/home/user/actual_output.txt`.

**Provided Environment:**
Assume that `/home/user/tests/` exists and contains various `.sm` files. You do not need to create these test files, just ensure your `test.sh` processes whatever `.sm` files are in that directory.

Ensure all three `.sh` scripts (`build.sh`, `run_interpreter.sh`, `test.sh`) are placed directly in `/home/user/` and have executable permissions.