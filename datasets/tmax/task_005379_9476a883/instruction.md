You are a data scientist working on an experimental physics project. You need to analyze experimental video data and build a robust model-fitting tool in C that handles near-singular matrices using Tikhonov regularization.

**Step 1: Experimental Data Analysis**
We have captured experimental footage located at `/app/experiment.mp4`. 
1. Use standard command-line tools (like `ffmpeg` and `ffprobe`) to determine the exact total number of frames in this video.
2. Write this integer frame count to a file named `/home/user/frame_count.txt`.

**Step 2: Robust Matrix Solver**
During model fitting, we frequently encounter near-singular 2x2 matrices that cause standard solvers to fail. You need to implement a regularized solver in C.
Write a C program at `/home/user/solve_system.c` and compile it to an executable named `/home/user/solve_system`. 

The program must:
1. Read exactly 7 double-precision floating-point numbers from standard input (whitespace-separated) in this order:
   `A11 A12 A21 A22 b1 b2 lambda`
   This represents a 2x2 matrix `A`, a 2x1 vector `b`, and a regularization parameter `lambda`.
2. Solve the regularized normal equations: `(A^T * A + lambda * I) * x = A^T * b`, where `I` is the 2x2 identity matrix.
3. Compute the 2x1 solution vector `x` (components `x1` and `x2`).
4. Print `x1` and `x2` to standard output, separated by a single space, formatted to exactly 6 decimal places (i.e., `%.6f %.6f\n`).

**Requirements:**
- Ensure your C code is numerically stable and uses double-precision math.
- The executable must be located at `/home/user/solve_system`.
- Do not print any other text or prompts to standard output.

We will verify your C program by fuzzing it against a known-correct oracle implementation over thousands of random inputs to ensure bit-exact equivalence.