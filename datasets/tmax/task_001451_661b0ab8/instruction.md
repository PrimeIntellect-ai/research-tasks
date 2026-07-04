You have just inherited an unfamiliar codebase for a custom numerical relaxation engine, located at `/home/user/nbody_relax`. The previous developer left abruptly, and the project is currently in a broken state. 

Your goals are to recover lost configuration data, fix a mathematical convergence bug in the engine, and prove the fix works with a minimal reproducible example (MRE).

Here are the specific issues you need to resolve:

1. **Git History Forensics (Secret Recovery):**
   The previous developer mentioned a "magic convergence seed" (a specific 32-character hexadecimal string) that was temporarily hardcoded into the project for calibration. It was later "scrubbed" from the latest commits for security reasons, but the simulation fails without it. 
   - Dig through the git repository's history at `/home/user/nbody_relax` to find this 32-character hex string.
   - Save the exact 32-character string (and nothing else) to a file named `/home/user/magic_seed.txt`.

2. **Convergence Failure Repair:**
   The core solver in `/home/user/nbody_relax/solver.c` implements a Newton-Raphson method to find the root of a specific polynomial. However, it currently hits the maximum iteration limit (fails to converge) or produces `NaN` values. 
   - Analyze the C code in `solver.c`. Look carefully at the iterative update step. There is a critical mathematical or type-casting bug preventing convergence.
   - Fix the bug directly in `/home/user/nbody_relax/solver.c`. 

3. **Minimal Reproducible Example (MRE):**
   To prove the system is fixed, you must write a standalone C program that utilizes the repaired logic.
   - Create a file at `/home/user/mre.c`.
   - This program must include or link to your fixed logic from `solver.c`.
   - In the `main` function, initialize the solver with a starting guess of `x = 10.0` and a target offset of `25.0`.
   - Execute the solver.
   - Print the final converged result (as a floating-point number formatted to 4 decimal places, e.g., `5.0000`) to a file named `/home/user/convergence_result.txt`.
   - The program must compile successfully to `/home/user/mre` (e.g., using `gcc -o /home/user/mre /home/user/mre.c /home/user/nbody_relax/solver.c -lm`) and exit with code 0.

Ensure all outputs are placed exactly at the specified absolute paths.