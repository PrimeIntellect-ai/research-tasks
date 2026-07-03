You have recently inherited an unfamiliar data processing codebase written in C. The main binary is supposed to process 64-bit unsigned integers and output a transformed hash based on a specific mathematical formula.

However, the current implementation in `/home/user/compute.c` has a couple of major issues:
1. It crashes and dumps core on certain edge-case inputs.
2. It suffers from numerical instability/signed integer overflow on x86_64, producing incorrect results for larger inputs.

You have been provided with a design specification image at `/app/spec.png`. This image contains the exact formula and constraints the program is supposed to implement. 

Your task:
1. Extract the text/specification from `/app/spec.png` (OCR tools like `tesseract` are preinstalled).
2. Diagnose the core dump and stack trace issues in `/home/user/compute.c`.
3. Fix the numerical instability (signed integer overflow) and crashing bugs. All intermediate logging and tracebacks should be removed in the final executable.
4. The final fixed C program must be compiled as a standalone executable at `/home/user/compute_fixed`. It should take exactly one command-line argument (the integer input as a string) and print the computed unsigned 64-bit integer to standard output, followed by a newline.

Your compiled `/home/user/compute_fixed` will be automatically tested against a reference oracle using an extensive fuzzing equivalence verifier with thousands of random 64-bit integer inputs. Bit-exact equivalence in the output is strictly required.