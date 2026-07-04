You have inherited an unfamiliar C codebase from a former developer. One of the core utilities is a small program located at `/home/user/event_parser.c`. This program calculates a custom index used to bucket logs based on the days since an epoch, the hour of the day, and the timezone offset.

Recently, the containerized application using this utility has been crashing intermittently. The logs indicate that the C program occasionally fails an internal assertion and aborts, particularly for events occurring very early in the epoch with negative timezone offsets. 

Your task is to:
1. Examine `/home/user/event_parser.c` and understand the formula being used. The code contains an assertion-based validation step that is failing.
2. Identify the subtle formula implementation bug. (Hint: consider how C handles certain arithmetic operations on negative numbers compared to other languages like Python).
3. You may want to write a quick fuzzing script to find the exact combination of inputs that trigger the crash to confirm your hypothesis.
4. Fix the formula in `/home/user/event_parser.c` so that it correctly and safely computes the index under all valid inputs. The resulting index must *always* be strictly between 0 and 1023 (inclusive).
5. Recompile the program: `gcc -o /home/user/event_parser /home/user/event_parser.c`
6. Run the fixed program with the following arguments: `days_since_epoch=0`, `hour=4`, `timezone_offset=-8`.
7. Save the exact numeric output of this specific run to a file named `/home/user/solution.txt`.

Do not change the signature of the `calculate_index` function or the CLI argument parsing logic. Only fix the mathematical calculation inside the function.