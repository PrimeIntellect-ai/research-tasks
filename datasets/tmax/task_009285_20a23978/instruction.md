You are acting as a data scientist's assistant. We are fitting a biochemical model, but our numerical ODE integrator in C is currently diverging and producing `NaN` values due to incorrect step-size adaptation logic.

Your task:
1. Inspect the C source code located at `/home/user/simulator.c`. It implements an adaptive explicit ODE solver for a 2D system.
2. Identify and fix the bug in the step-size adaptation logic. The integrator currently increases the step size when the local truncation error is too high, which causes divergence. It should do the exact opposite.
3. Compile the fixed C program and run it. It is programmed to write the integrated state variable `Y` at specific time intervals to `/home/user/output.txt`.
4. We need to measure how well our simulated distribution matches our empirical reference dataset. Use the provided Python script `/home/user/evaluate.py` to calculate the Kullback-Leibler (KL) divergence between your `output.txt` and the reference data `/home/user/ref_data.txt`.
   Command usage: `python3 /home/user/evaluate.py /home/user/output.txt /home/user/ref_data.txt`
5. Save the single floating-point number output by `evaluate.py` into a new file at `/home/user/result.txt`.

Ensure `/home/user/result.txt` contains only the numeric KL divergence value.