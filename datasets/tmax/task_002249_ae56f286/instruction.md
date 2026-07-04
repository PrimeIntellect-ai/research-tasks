You are an operations engineer triaging an incident. Our primary metric calculation pipeline is completely broken after a botched deployment. 

You need to restore the pipeline by fixing the compilation of our helper tool and correcting the mathematical logic in the main Bash script.

Here is the situation:
1. The original mathematical formula was lost from our database, but a developer managed to capture a screenshot of the correct quadratic formula before the system went down. This screenshot is located at `/app/formula.png`.
2. The pipeline relies on a C helper utility located in `/home/user/src/`. However, running `make` in that directory currently fails with a linker error.
3. The current script `/home/user/pipeline.sh` is outputting incorrect values because the coefficients and signs in the math logic are wrong.

Your task:
1. Extract the correct mathematical formula from the image at `/app/formula.png`.
2. Diagnose and fix the compiler/linker error in `/home/user/src/Makefile` so that the `helper` binary compiles successfully.
3. Write a new, fixed pipeline script at `/home/user/fixed_pipeline.sh` that takes a single integer argument `x` and prints the calculated integer result `y` to standard output. 
4. The `fixed_pipeline.sh` script must strictly follow the formula recovered from the image. You may use standard bash arithmetic and/or the compiled `helper` tool (which calculates $x^2$) to compute the result.

Make sure `/home/user/fixed_pipeline.sh` is executable and cleanly outputs only the final integer.