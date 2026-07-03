You are a performance engineer profiling a numerical application. A legacy Bash-based signal simulator, which uses the Euler method to integrate a high-frequency system, is experiencing severe numerical instability. The integration diverges because the default step size is too large for the system's stiffness.

The simulation script is located at `/home/user/app/simulate_ode.sh`. It accepts a single argument: the step size `h` (defaulting to 0.1). It prints the time and the integrated signal value space-separated to standard output. 

Your task is to write a bash script at `/home/user/app/find_stable_step.sh` that implements a simple step-size adaptation (profiling) routine to find the largest stable step size.

Requirements for `/home/user/app/find_stable_step.sh`:
1. It must start testing with an initial step size of `h = 0.1`.
2. For each `h`, run `/home/user/app/simulate_ode.sh $h` and capture the output.
3. Determine if the simulation is numerically stable. A simulation is considered stable for this system if the maximum absolute value of the signal (column 2) remains strictly less than `100.0`.
4. If the simulation diverges (max absolute value >= 100.0), halve the step size (`h = h / 2`) and try again.
5. Once the first stable `h` is found, the script should terminate the search and write a summary to `/home/user/app/stability_log.txt`.

The output in `/home/user/app/stability_log.txt` must exactly match the following format:
`Stable h: <found_h>, Max Val: <max_absolute_value>`

Example format:
`Stable h: 0.003125, Max Val: 1.0`

Please ensure your `find_stable_step.sh` is executable and run it to produce the final `stability_log.txt`. Use standard Bash tools (`awk`, `bc`, etc.) for all mathematical comparisons.