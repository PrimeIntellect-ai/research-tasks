I've inherited an unfamiliar project that implements a highly specialized mathematical expression evaluator used for fluid dynamics simulations. Unfortunately, the previous developer accidentally deleted the crucial header file (`expr_parser.h`) and left the main C++ implementation (`math_evaluator.cpp`) with several format parsing bugs and compiler/linker errors. 

We do have an older compiled version of the evaluator, but it is a stripped binary located at `/app/math_oracle`. 

Your task is to:
1. Recover the deleted header file. I managed to dump the filesystem partition into an image file at `/home/user/ext4_dump.img`. You will need to inspect this image or recover the deleted `expr_parser.h` file from it.
2. Fix the compiler and linker errors in the existing `/home/user/src/math_evaluator.cpp` and the recovered header. You'll likely see errors about missing standard library linkages and undefined references.
3. The parser in `math_evaluator.cpp` has edge-case bugs when handling nested parentheses and consecutive operators (like `5 * -3` or `(2+(3))*4`). Write a fuzzer to generate random mathematical expressions and compare the output of the compiled `math_evaluator` against the `/app/math_oracle` binary to find and fix these edge-case bugs in the parser.
4. Output a fully working program that takes a single mathematical expression as a command-line argument and prints the floating-point result to standard output. Save the final compiled executable to `/home/user/final_evaluator`.

The automated test will generate 1000 complex mathematical expressions, run both your `/home/user/final_evaluator` and `/app/math_oracle`, and compare the numerical results. To pass, your implementation must achieve at least a 99% match rate with the oracle.