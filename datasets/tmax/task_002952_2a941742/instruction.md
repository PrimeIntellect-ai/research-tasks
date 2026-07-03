You have inherited an unfamiliar C codebase located in `/home/user/project`. The program is designed to read a sequence of integers from standard input, compute a custom moving-window weighted checksum, and print the results to standard output. 

Unfortunately, the previous developer left before completing it. They left behind a compiled reference binary (the "oracle") at `/app/oracle_bin` that represents the correct behavior, and a screenshot of the mathematical specification located at `/app/kernel_spec.png`.

Your objectives are:
1. Extract the integer weights from the image `/app/kernel_spec.png` (you can use tools like `tesseract` which are available in the environment) and integrate them into the C codebase.
2. The current C code is highly unstable. It suffers from several issues:
   - It segfaults or behaves unpredictably when encountering corrupted input (e.g., non-numeric ASCII characters mixed with numbers). It is supposed to gracefully ignore non-numeric tokens.
   - It has an off-by-one error in its boundary condition, causing it to drop or incorrectly compute the last window of data.
   - It occasionally produces intermittent failures due to uninitialized memory.
3. Diagnose and fix the C source code. You are strongly encouraged to write a shell-based fuzz testing script that feeds random numbers and corrupted tokens into both your compiled program and `/app/oracle_bin` to identify differences and regression-test your fixes.
4. Compile your final, fixed program to exactly `/home/user/fixed_bin`.

The final executable `/home/user/fixed_bin` must be functionally identical (bit-exact output) to `/app/oracle_bin` across any arbitrary input stream. Do not modify or move the reference binary or the image.