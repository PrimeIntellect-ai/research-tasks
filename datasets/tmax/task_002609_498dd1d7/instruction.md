You are tasked with implementing a critical curve-fitting module for a reproducible scientific computation pipeline. We are modeling phenomena over a finite field, and need a C++ program that exactly interpolates three data points using a quadratic model: $y \equiv C_0 + C_1 x + C_2 x^2 \pmod p$.

Your tasks:
1. **Extract Pipeline Parameters**: The Lead Data Scientist left an audio dictation with the required prime modulus $p$ and the exact required output formatting string. You can find this recording at `/app/dictation.wav`. You must process this audio file to extract these two pieces of information.
2. **Implement the Curve Fitter**: Write a C++ program at `/home/user/poly_fit.cpp` and compile it to an executable at `/home/user/poly_fit`. 
   - The program must accept exactly six integer command-line arguments: `x1 y1 x2 y2 x3 y3`.
   - It must compute the coefficients $C_0, C_1, C_2$ of the quadratic polynomial that perfectly passes through these three points over the finite field of the prime modulus $p$ extracted from the audio.
   - All arithmetic must be performed modulo $p$. You may assume the inputs will always be provided such that $x_1, x_2, x_3$ are distinct modulo $p$.
   - The output must be printed to standard output exactly matching the format dictated in the audio file.
3. **Compile**: Ensure your executable is compiled with `g++ -O3 /home/user/poly_fit.cpp -o /home/user/poly_fit`.

Your executable will be subjected to rigorous automated regression testing (fuzzing) against thousands of random valid inputs to ensure bit-exact equivalence with our reference oracle.

Do not wrap the output in quotes or add extra newlines beyond a standard trailing newline.