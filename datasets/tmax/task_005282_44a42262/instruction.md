I am working on a scientific simulation project that calculates the impact time of a projectile using the quadratic kinematic equation, but my CI build is failing. 

The project is located in `/home/user/trajectory`. 
It consists of:
- `main.c`: Parses arguments and calls the calculation function.
- `calc.c`: Contains the `calculate_impact_time(double a, double b, double c)` function.
- `calc.h`: Header file.
- `build.sh`: A shell script to compile the project.
- `fuzzer.sh`: A bash script that fuzzes the compiled executable with various extreme floating-point inputs to check for accuracy against a known safe python baseline.

Here is what I need you to do:
1. First, `build.sh` is failing to compile the code. Diagnose and fix the build environment/script misconfiguration so that it successfully produces the executable `traj_calc`.
2. Run `./fuzzer.sh`. You will notice it fails on certain edge cases. The `calculate_impact_time` function in `calc.c` calculates the smallest positive root of the quadratic equation $at^2 + bt + c = 0$. However, the current implementation uses a naive formula that suffers from severe floating-point catastrophic cancellation when $b$ is large and $a$ and $c$ are very small. It might also be incorrectly casting to single-precision `float` internally.
3. Fix `calc.c` by correcting the mathematical formula to avoid catastrophic cancellation (hint: use the mathematically equivalent formula that multiplies by the conjugate, or use the stable quadratic formula using $q = -0.5 \times (b + \text{sgn}(b)\sqrt{b^2 - 4ac})$) and ensure all calculations retain double precision.
4. Verify your fix by running `./build.sh` and ensuring `./fuzzer.sh` passes without any errors.
5. Once the fuzzer passes, run the executable manually with the following inputs: `./traj_calc 0.0001 1000.0 0.0001`.
6. Save the exact console output of that command into a file at `/home/user/final_output.txt`.

The format of `/home/user/final_output.txt` should be exactly the output printed by the `main.c` wrapper (e.g., a single floating point number).