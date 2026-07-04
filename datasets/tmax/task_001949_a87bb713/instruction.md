You are an engineer tasked with porting a legacy mathematical tool to run inside a minimal, scratch-based container. The tool calculates the determinant of a square matrix using Gaussian elimination (LU decomposition). 

Currently, the source code is located at `/home/user/math_port/det_calc.c`. However, it has two critical issues that prevent it from being production-ready:
1. **Memory Leak**: The tool dynamically allocates memory for the matrix but fails to free it properly before exiting. This causes container OOM issues in long-running batches.
2. **Numerical/Algorithmic Bug**: When performing row swaps during the elimination step, the code fails to track the sign of the determinant. Each row swap should flip the sign of the determinant, but the current implementation ignores this, leading to incorrect absolute values or incorrect signs for some inputs.

Your objectives are:
1. **Fix the code**: Modify `/home/user/math_port/det_calc.c` to resolve both the memory leak and the row-swap sign bug.
2. **Compile statically**: Create a Makefile at `/home/user/math_port/Makefile` that compiles `det_calc.c` into a statically linked executable named `det_calc` (this is required for the minimal container environment). It should link the math library.
3. **Property-based Verification**: We have provided a Python script using the `hypothesis` library at `/home/user/math_port/verify_props.py`. This script feeds random matrices into your compiled binary and checks two properties:
   - $det(A \times B) = det(A) \times det(B)$
   - Valgrind reports 0 bytes lost.
   Run `python3 /home/user/math_port/verify_props.py`. If successful, the script will create a file at `/home/user/math_port/verification.log` containing the word `SUCCESS`.

Ensure `/home/user/math_port/verification.log` is successfully created and contains `SUCCESS`.