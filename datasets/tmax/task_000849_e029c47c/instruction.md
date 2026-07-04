You are a data scientist tasked with building a robustness filter for a legacy numerical simulation pipeline. 

We have a proprietary compiled numerical integrator located at `/app/integrator_bin`. Unfortunately, the source code was lost, and it has been stripped of symbols. This binary simulates a complex physical system's trajectory. It takes an input parameter file and writes the simulated trajectory to an output file. From some basic testing, we know it is invoked as:
`/app/integrator_bin <input_params.csv> <output_trajectory.csv>`

For certain initial conditions, the internal step-size adaptation of the integrator fails, causing the simulation to silently diverge. When it diverges, the resulting trajectory data exhibits subtle heavy-tailed distributions and anomalous variance compared to stable runs, even if the values don't overflow to NaN.

Your task is to create a Python anomaly detector (`/home/user/detector.py`) that acts as a filter to reject inputs that cause divergence.

To do this, you must:
1. Compile and install the custom probability distance metric library provided in source form at `/app/libdist/`. This C-extension (which provides a fast custom Wasserstein-like metric) must be built and installed in your Python environment.
2. Write a script at `/home/user/detector.py` that takes exactly one argument: the path to an input CSV parameter file.
3. Your script should:
   a. Invoke `/app/integrator_bin` with the provided input file and a temporary output file.
   b. Load the multi-dimensional trajectory data from the output.
   c. Use bootstrap confidence intervals of the trajectory's spatial variance, combined with density estimation (using the compiled `libdist` module's `compute_distance` function compared against a standard normal distribution), to determine if the run diverged.
   d. Exit with code `0` if the trajectory is STABLE (clean).
   e. Exit with code `1` if the trajectory DIVERGES (evil/anomalous).

We have provided two directories of example input parameters:
- `/app/data/clean/`: Contains inputs that result in stable, physically valid trajectories.
- `/app/data/evil/`: Contains inputs that cause the numerical integrator's step-size to break down, resulting in divergent trajectories.

Your detector must correctly classify 100% of the files in both corpora. An automated verifier will test your script against hidden datasets generated from the same distributions.

Constraints:
- Use Python 3.
- You must use the `libdist` module compiled from source.
- Do not modify the input parameter files or the binary.