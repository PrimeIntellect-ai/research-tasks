You are tasked with debugging a failing build for a legacy C physics tool. 

The project is located at `/home/user/astro_calc`. Currently, if you try to build it using `make`, it fails with a linker error. 

Your objectives are:
1. **Fix the Linker Error:** Diagnose and fix the build issue in the `Makefile` so the project compiles successfully.
2. **Fix Precision Loss:** The compiled program currently outputs a highly inaccurate result due to recent changes that introduced precision loss in the intermediate state calculations.
3. **Recover the Secret Constant:** The precision loss was caused by someone accidentally downgrading the variables to `float` and replacing the high-precision `CALIBRATION_SECRET` constant with a truncated version. The original high-precision constant (a `double` value with 10+ decimal places) is buried somewhere in the Git history of the repository.
4. **Output the Correct Result:** Restore the high-precision constant from the Git history, fix the code in `calc.c` to use `double` for all calculations to avoid intermediate precision loss, and recompile.

Once you have fixed the code and compiled it, run `./astro_calc` and redirect its standard output to exactly this file: `/home/user/fixed_output.txt`.

The format of `/home/user/fixed_output.txt` should be exactly the output of the program, which looks like: `Trajectory: <value>`.