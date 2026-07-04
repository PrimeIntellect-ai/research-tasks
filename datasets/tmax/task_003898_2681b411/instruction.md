You are tasked with debugging a failing C project for a mathematical sequence generator.

A developer was attempting to re-implement a proprietary calculation tool. The reference implementation is provided as a stripped binary at `/app/oracle_bin`. The developer's work-in-progress code is located in `/home/user/project/`.

Currently, the project fails to build. Even if you force it to compile by guessing the developer's intent, running it with certain inputs causes it to crash with a segmentation fault (core dump).

Your task is to:
1. Fix the build process in `/home/user/project/` so that running `make` successfully produces an executable named `solution`.
2. Debug the runtime crash. You will need to analyze the logic, fix the recursion/loop termination issue, and ensure it correctly calculates the sequence without overflowing the stack.
3. Ensure the output of your fixed program perfectly matches the output of the reference binary `/app/oracle_bin` for any non-negative integer input. 

The executable `/home/user/project/solution` must accept a single non-negative integer as a command-line argument and print a single unsigned integer to standard output, exactly like the oracle.

To complete the task, leave the fully fixed and compiled `solution` executable in `/home/user/project/`.