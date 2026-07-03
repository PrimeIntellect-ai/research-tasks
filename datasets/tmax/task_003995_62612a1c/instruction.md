You are an operations engineer triaging an incident where a critical simulation model has started failing to converge after a configuration update. 

You have been provided with the source code for the simulation model at `/home/user/sim_model.c` and the failing configuration file at `/home/user/config.txt`.

Your tasks are:
1. **Compile the Model**: The model requires standard compilation but might throw linker errors if not linked properly. Produce an executable named `/home/user/sim_model`.
2. **Delta Debugging**: The current `config.txt` causes the model to fail to converge (the program exits with code 1). Write a script in a language of your choice to systematically minimize `config.txt` and find the absolute minimum set of configuration lines that still causes the program to exit with code 1. Save this minimal configuration to `/home/user/min_config.txt`.
3. **Convergence Repair**: Once you identify the problematic parameters, create a `/home/user/fixed_config.txt`. This file should be identical to the original `config.txt`, but with the value of `BETA` changed to `0.5` to restore convergence (the program should exit with code 0).

Constraints:
- The `sim_model` executable expects the configuration file to be named `config.txt` in the current working directory.
- `/home/user/min_config.txt` must contain only the lines necessary to trigger the failure.

Please complete these steps and ensure the required files are present.