You are acting as a support engineer diagnosing a hanging background process. We have a C-based data processing tool located at `/home/user/processor.c`. It reads comma-separated records from standard input and prints processed results. 

Recently, a customer provided a large dataset (`/home/user/large_input.txt`) that causes the program to hang indefinitely. There are also reports that the mathematical formula for calculating the "Weight" of each record is incorrect.

Your task is to:
1. Identify the minimal input that causes the hang. Find the exact single line from `large_input.txt` that triggers the infinite loop, and save this single line to `/home/user/minimal_crash.txt`.
2. Modify `/home/user/processor.c` to fix the infinite loop. The loop processes data in chunks based on the `length` field. If a corrupted record has `length <= 0`, the program currently hangs. Fix it so that if `length <= 0` inside the loop, it immediately prints `Corrupted record ID: <id>\n` (where `<id>` is the record's ID) and stops processing that specific record, moving on to the next one.
3. Correct the "Weight" calculation formula in `/home/user/processor.c`. The correct formula is `Weight = a + (b * c)`. The current implementation has a bug in the operator precedence or grouping.
4. Compile your fixed C program to `/home/user/processor`.
5. Run the fixed program using `/home/user/large_input.txt` as standard input, and redirect the output to `/home/user/fixed_output.txt`.

Ensure your C code compiles without errors using `gcc -O2 processor.c -o processor`.