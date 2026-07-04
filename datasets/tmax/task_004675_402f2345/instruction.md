` to explicitly define the inputs, the parallelization requirement, and the exact output format. In the `<truth>` block, I will define the exact metric and the binary's behavior to fulfill the `metric_threshold` and `stripped_binary` axes.

<task>
You are a data scientist fitting a complex spectroscopic model to experimental data. 

We have an ultra-fast, optimized legacy simulation engine provided as a compiled binary at `/app/bin/spectral_sim`. This binary takes three float parameters (`alpha`, `beta`, `gamma`) representing sequence-binding affinities (each bounded between 0.0 and 10.0), and outputs a simulated spectral signature consisting of 1024 space-separated float values.

Your target experimental data is located at `/app/data/experimental_spectrum.txt` (a single line of 1024 space-separated floats).

Your task is to find a set of parameters `(alpha, beta, gamma)` that produces a simulated spectrum closely matching the experimental spectrum. 

Requirements:
1. Distance Metric: Use the 1-Wasserstein distance (from `scipy.stats.wasserstein_distance`) between the simulated spectrum and the experimental spectrum to evaluate fitness.
2. Parallelization: Since the parameter space is large, you must write a Python script that uses parallel computing (e.g., `multiprocessing` or `concurrent.futures`) to perform a grid search, random search, or optimization over the parameter space `[0.0, 10.0]` for each variable.
3. Threshold: You must find a parameter combination that results in a Wasserstein distance of less than or equal to 0.15.
4. Output: Once you find parameters that satisfy this threshold, write them to `/home/user/best_params.csv` in the format: `alpha,beta,gamma` (a single line, comma-separated floats).

You will need to install any necessary Python packages, write the optimization script, and execute it to find the solution. The legacy binary has no documentation and has been stripped of symbols; treat it as a black-box oracle.