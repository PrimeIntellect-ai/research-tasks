You are a performance engineer profiling a scientific simulation application. The C++ simulator processes a sequence of movement commands to calculate the final position of a particle. Currently, the application fails on a large dataset due to floating-point precision issues accumulating over time, causing it to fail validation checks. 

Your tasks are:
1. Investigate the C++ source code located at `/home/user/sim_project/simulator.cpp`.
2. Identify and fix the floating-point precision bug. The simulation state is currently accumulating errors because it uses single-precision `float` for the particle's position and calculations, which loses precision over millions of simulated micro-steps. 
3. Upgrade the necessary variables to double-precision (`double`) to resolve the precision loss.
4. Compile the fixed program using the provided `Makefile` in `/home/user/sim_project/`.
5. Run the compiled `./simulator` on the input file `/home/user/sim_project/large_input.txt`.
6. The program will output a final validation result. Write the exact final calculated position (printed by the fixed program on the last line, format: `FINAL: <value>`) to a file named `/home/user/result.txt`.

Ensure your fix strictly addresses the data type precision of the accumulating position without altering the mathematical logic or input parsing.