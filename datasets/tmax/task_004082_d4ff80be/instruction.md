You are a data scientist working with a legacy, poorly-documented mathematical model solver. We are trying to orchestrate a large-scale parameter sweep for our ODE model using a bash-driven pipeline, but the core engine keeps crashing on certain parameter combinations, bringing down the whole pipeline.

The core engine is a stripped binary located at `/app/solve_ode`. It simulates a nonlinear dynamical system.
It takes a single configuration file as an argument: `/app/solve_ode <config_file>`.

The configuration files contain three parameters, formatted exactly like this (with floating point numbers):
```
alpha=1.5
beta=2.0
gamma=0.5
```

When given "good" parameters, the binary runs successfully and outputs the final state of the ODE. 
When given "bad" parameters, the binary either suffers a Segmentation Fault, a Floating Point Exception, or hangs in an infinite loop due to equation stiffness. 

Your task:
1. Reverse engineer or black-box test the `/app/solve_ode` binary to determine the exact mathematical conditions under which the parameters (`alpha`, `beta`, `gamma`) cause the program to crash or fail.
2. Write a Bash script located at `/home/user/filter.sh` that acts as a sanitizer/classifier for our parameter sweep. 
3. The script MUST take a single file path as its first argument: `/home/user/filter.sh <path_to_config_file>`.
4. The script MUST read the parameters from the file, evaluate them against the rules you deduced, and exit with code `0` if the parameters are safe (the binary will run successfully), and exit with code `1` if the parameters are unsafe (the binary would crash).
5. The script MUST NOT actually run the `/app/solve_ode` binary during classification, as invoking the binary is too slow for our multi-million file parameter sweep. It must evaluate the mathematical constraints directly in Bash (using tools like `awk` or `bc`).

To help you test, you can create your own dummy configuration files and test them against `/app/solve_ode`. Do not alter the binary itself.