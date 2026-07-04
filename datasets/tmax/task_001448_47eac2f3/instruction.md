You are a security researcher analyzing a suspicious token generation binary. You have intercepted the source code (`/home/user/auth_gen.c`) and a large log file of intercepted timestamps and timezones (`/home/user/traffic.log`).

When you compile and run the program against `traffic.log`, it crashes with a Segmentation Fault before completing. Furthermore, initial static analysis suggests the mathematical formula used to calculate the timezone-adjusted time has a subtle error, causing the generated tokens to be incorrect even when the program doesn't crash.

Your objectives:
1. **Delta Debugging / Crash Analysis:** Find the specific malformed line(s) in `/home/user/traffic.log` causing the segmentation fault. Use GDB or test minimization to isolate the fault.
2. **Fix the Crash:** Modify `/home/user/auth_gen.c` to properly handle long timezone strings without memory corruption.
3. **Formula Implementation Correction:** There is a logical error in how the timezone offset is calculated in `auth_gen.c`. We have provided a test script `/home/user/verify_tokens.py` that validates the logic against a few known-good timestamp/timezone pairs. Fix the formula in `auth_gen.c` until `python3 /home/user/verify_tokens.py` reports success.
4. **Final Execution:** Once the C code is completely fixed and compiled, run it against a new set of inputs located at `/home/user/target_traffic.txt`.
5. **Output Requirement:** Redirect the standard output of your fixed program running against `target_traffic.txt` to exactly `/home/user/final_tokens.log`.

Do not change the `printf` output format in the C code, only fix the buffer overflow and the mathematical logic for the offset calculation. Compile the C code using `gcc -g -o /home/user/auth_gen /home/user/auth_gen.c`.