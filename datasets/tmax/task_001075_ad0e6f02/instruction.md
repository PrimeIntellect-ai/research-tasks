I am a researcher studying the orbital decay of a hypothetical binary star system. I lost the source code for my numerical integrator, and I only have a compiled, stripped binary located at `/app/binary_integrator`. 

This binary takes four arguments: `initial_radius`, `initial_velocity`, `time_step`, and `num_steps`. It simulates the system using a custom adaptive step-size Euler method and outputs the final radius and velocity to standard output. 

Your task is to:
1. Analyze the `/app/binary_integrator` to understand the exact numerical integration algorithm and its specific step-size adaptation logic. The adaptation has a known quirk where it diverges if the step size grows beyond a certain threshold.
2. Write a pure Bash script (using `awk` or `bc` is allowed) at `/home/user/replicated_integrator.sh` that takes the exact same four arguments and produces the exact same output (bit-exact string match) as the stripped binary for any valid floating-point inputs.
3. The script must handle data parsing and reproduce the simulation perfectly.

Make sure `/home/user/replicated_integrator.sh` is executable and accepts inputs like: `./replicated_integrator.sh 10.0 0.5 0.01 100`.