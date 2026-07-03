You are a QA engineer tasked with setting up a verification environment for a legacy system. We have a proprietary domain-specific language (DSL) used to define memory-lifetime constraints. Currently, our main test script (`/home/user/qa_env/test_case.lt`) is failing due to constraint violations. 

Developers have provided a set of candidate patches in `/home/user/qa_env/patches/`, but they don't know which one actually resolves all lifetime constraints correctly without introducing new errors.

Your task has three phases:

**Phase 1: Build the Emulator**
Write a Python script at `/home/user/emulator.py` that acts as an interpreter for our `.lt` DSL. The script must accept a single file path as a command-line argument and execute the DSL line-by-line. 

The DSL has the following commands:
- `ALLOC <var>`: Marks the variable `<var>` as ALIVE. If `<var>` is already ALIVE, the emulator must immediately halt with an error (exit code 1) for a "Double Alloc".
- `FREE <var>`: Marks `<var>` as DEAD. If `<var>` is already DEAD or was never ALOCATED, halt with an error (exit code 1) for a "Double Free" or "Uninitialized Free".
- `USE <var>`: Reads `<var>`. If `<var>` is DEAD or was never allocated, halt with an error (exit code 1) for a "Use After Free" or "Uninitialized Use".
- Lines starting with `#` or empty lines should be ignored.
- If the script reaches the end of the file without any errors, it must exit with code 0.

**Phase 2: Patch Processing**
You have been provided with multiple patch files (`patch_1.diff` through `patch_10.diff`) in the `/home/user/qa_env/patches/` directory. These patches are designed to be applied to `/home/user/qa_env/test_case.lt`.

**Phase 3: Constraint Satisfaction**
Using your emulator and standard Bash tools (like `patch`), determine which *single* patch successfully resolves all lifetime constraints in `test_case.lt` (i.e., your emulator exits with code 0). 

Once you identify the correct patch, write the exact filename of the successful patch (e.g., `patch_4.diff`) to a log file at `/home/user/success.log`. 

Ensure `/home/user/emulator.py` is fully functional and remains on the system.