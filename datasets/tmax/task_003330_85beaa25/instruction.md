You are a bioinformatics analyst tasked with evaluating sequence primers using a novel regularized position-weight model. 

We have received an experimental 4x4 substitution matrix encoded visually in a video file located at `/app/matrix.mp4`. The video is exactly 16 seconds long, at 1 frame per second. Each frame consists of a uniform grayscale solid color.

Your task is to build a C program that computes a numerically stable profile vector for a given DNA primer sequence, using the data from this video.

**Step 1: Observational Data Reshaping**
Extract the average grayscale intensity (0-255) of each frame in the video. 
Map these 16 values sequentially into a 4x4 matrix $M$ in row-major order. The rows and columns correspond to the nucleotides A, C, G, and T respectively. Normalize the matrix by dividing each entry by 255.0.

**Step 2: Numerical Stability & Sequence Profiling**
The experimental matrix $M$ is known to be near-singular, which causes standard linear sequence transformations to fail. 
Write a C program that takes a single DNA sequence string (containing only A, C, G, T) as its first command-line argument (`argv[1]`).
Your program must:
1. Count the occurrences of A, C, G, and T in the input string to form a 4-element column vector $b$.
2. Calculate the stable primer component weights $x$ by solving the Tikhonov-regularized least squares problem:
   $(M^T M + \lambda I) x = M^T b$
   where $\lambda = 0.05$ is the regularization parameter, and $I$ is the 4x4 identity matrix.
3. Print the four components of $x$ (for A, C, G, T) to standard output on a single line, separated by spaces, formatted to exactly 6 decimal places (e.g., `0.123456 0.000000 1.234567 -0.555555`).

**Step 3: Implementation**
Save your C code at `/home/user/eval_primer.c`.
Compile it to an executable at `/home/user/eval_primer` using standard math libraries if necessary (`-lm`).
Ensure your program compiles without errors and strictly matches the expected output format. Do not print any other debug text to standard output.