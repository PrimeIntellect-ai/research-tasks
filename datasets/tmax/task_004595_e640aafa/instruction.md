You are a performance engineer tasked with modernizing and profiling a legacy physics application. We have a stripped legacy binary located at `/app/profiler_sim` which performs a numerical simulation of a dynamical system.

This binary takes exactly one command-line argument: the path to an HDF5 file. 
The HDF5 file contains a single dataset named `/initial_state` containing exactly 3 double-precision floats: `[x0, v0, dt_base]`.
The binary reads these initial conditions, integrates the system until `t = 5.0` seconds using a custom (and numerically suspect) step-size adaptation logic, and prints the final `x` position to stdout.

We need to port this simulation to Python so we can run MCMC sampling and numerical stability tests on the step-size logic. 

Your task:
1. Analyze the `/app/profiler_sim` binary. You may use black-box curve fitting/regression to model its input-output relationship, or reverse-engineer the exact numerical integration loop using standard Linux tools (like `objdump`, `ltrace`, etc. which are available).
2. Create a Python script at `/home/user/solution.py` that takes the path to an input HDF5 file as its first argument.
3. Your Python script must read the `/initial_state` dataset, perform the exact same simulation algorithm, and print the resulting final position matching the binary's output exactly (including precision). 

The automated test will use an aggressive fuzzing verifier. It will generate dozens of random HDF5 files and assert that `/home/user/solution.py` produces the exact same standard output as `/app/profiler_sim`.

Ensure your Python script is robust and requires no user interaction.