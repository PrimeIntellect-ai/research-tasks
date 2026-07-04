You are an open-source maintainer reviewing a broken Pull Request. The PR attempts to add a small Python-based "bytecode emulator" that parses structured JSON instructions, validates execution constraints, and relies on a C shared library for computationally heavy "magic" operations. 

The contributor who opened the PR is unreachable, and the CI pipeline is failing on the test payload.

The workspace is located at `/home/user/pr_review/`.
Inside this directory, you will find:
- `src/processor.c`: A C file containing the math function `execute_magic`.
- `lib/libprocessor.so`: The compiled shared library from `processor.c`.
- `src/vm.py`: The bytecode emulator that parses instructions, verifies constraints, and calls the C library via `ctypes`.
- `tests/test_payload.json`: The structured data containing the bytecode instructions.

There are two major issues in `src/vm.py`:
1. **ABI Management Issue**: The `vm.py` emulator does not properly define the C-types ABI (arguments and return types) for the `execute_magic` function. Because the C function uses `double` precision floats, the default `ctypes` bindings are causing garbage memory calculations.
2. **Constraint Satisfaction Logic**: The `verify_constraints` function is supposed to reject execution if any `magic` instruction has an argument that is less than or equal to `0`, or if the argument is an odd number (not divisible by 2). The contributor messed up the boolean logic for this constraint check, causing valid payloads to be rejected with `CONSTRAINT_VIOLATION`.

Your task:
1. Fix the constraint logic and the `ctypes` ABI definitions in `/home/user/pr_review/src/vm.py`.
2. Run the emulator against the test payload: `python3 /home/user/pr_review/src/vm.py /home/user/pr_review/tests/test_payload.json`
3. If fixed correctly, the script will evaluate the emulator state and write the exact output to `/home/user/pr_review/output.log`. 

Ensure that the output file `/home/user/pr_review/output.log` is successfully created with the final calculated state. Do not modify the JSON payload or the C shared library.