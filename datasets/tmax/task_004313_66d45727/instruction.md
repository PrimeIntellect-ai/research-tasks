You are an AI assistant acting as a performance engineer for a bioinformatics group. We have a simple C file that calculates a primer alignment score, and we need to use this score to parameterize and profile an ODE model of PCR amplification.

Here is what you need to do:

1. **Compile the alignment tool**:
   You will find a C source file at `/home/user/align_score.c` (already created for you). Compile it into a shared library named `/home/user/libalign.so` using `gcc` (ensure it is compiled as position-independent code).

2. **Write the Profiling Script**:
   Create a Python script at `/home/user/profile_pcr.py` that does the following:
   * Uses `ctypes` to load `/home/user/libalign.so`.
   * Sets up the `get_score` function from the library to take two byte strings (`c_char_p`) and return an integer.
   * Calls `get_score` with the primer `"ATGCGTACG"` and the target sequence `"ATGCGTACA"` to get the alignment score.
   * Calculates the amplification rate parameter: $r = \text{score} / 10.0$.
   * Solves a logistic growth ODE representing PCR amplification: $dy/dt = r \cdot y \cdot (1 - y/1000)$.
     * Initial condition: $y(0) = 1$.
     * Time span: $t = 0$ to $t = 10$.
     * Use `scipy.integrate.solve_ivp`.
   * **Profiling**: Wrap *only* the `solve_ivp` function call using the `cProfile` module. Save the profiling statistics directly to a file named `/home/user/ode_profile.prof`.
   * Extract the final value of $y$ at $t = 10$ from the ODE solver's result, round it to exactly 2 decimal places (e.g., `123.45`), and write this final numeric value as a string to `/home/user/result.txt`.

Run your Python script to ensure all files (`libalign.so`, `ode_profile.prof`, and `result.txt`) are generated successfully.