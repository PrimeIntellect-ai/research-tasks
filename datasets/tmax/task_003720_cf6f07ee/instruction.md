You are a performance engineer tasked with profiling and regression-testing a legacy Monte Carlo particle diffusion simulator. 

We have a stripped, legacy binary located at `/app/mc_oracle`. This binary relies on both MPI and OpenMP for parallelization. Recently, users have reported that certain simulation configurations cause the application to silently produce invalid data (`NaN` or `0.0000`), crash, or deadlock indefinitely.

Your task is to write a robust Bash script at `/home/user/validate_config.sh` that acts as a regression test and classifier for simulation configuration files.

**Application Details:**
* The binary takes exactly one command-line argument: the path to a configuration file.
* A configuration file is a plain text file containing exactly three key-value pairs, one per line (e.g., `SAMPLES=1000000`, `RANKS=2`, `THREADS=4`).
* To correctly execute the binary, your script must extract `RANKS` and `THREADS` from the provided configuration file and invoke the binary using `mpirun`. 
* The execution command MUST follow this exact structure:
  `mpirun -np <RANKS> -x OMP_NUM_THREADS=<THREADS> /app/mc_oracle <path_to_config_file>`

**Script Requirements (`/home/user/validate_config.sh`):**
1. The script must accept exactly one argument: the path to the configuration file to be tested.
2. It must extract the `RANKS` and `THREADS` values from the given file to construct the MPI command.
3. It must execute the binary using the MPI command above, wrapping the execution with a 2-second timeout (using the `timeout` command) to catch deadlocks.
4. **Classification Logic:**
   * **Reject (Exit Code 1):** If the execution times out, returns a non-zero exit code, or if its standard output contains the strings `Result: NaN` or `Result: 0.0000`, the configuration is considered "evil"/invalid. Your script must exit with code `1`.
   * **Accept (Exit Code 0):** If the binary completes successfully within the timeout and produces valid numerical results, the configuration is "clean"/valid. Your script must exit with code `0`.

Ensure your script is executable (`chmod +x`). Do not modify the binary `/app/mc_oracle`. Use standard Linux tools (e.g., `grep`, `awk`, `timeout`) inside your Bash script.