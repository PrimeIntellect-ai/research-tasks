I need you to prepare a reproducible training dataset for our machine learning pipeline using our internal C++ simulation tool, and then expose some statistical metrics via an API.

We have a vendored C++ package located at `/app/fastsim-2.0.0`. It generates simulated particle regression data. Recently, the outputs have become non-reproducible (the floating-point reduction gives slightly different results or loses precision). The original author specifically implemented Kahan summation in `src/generator.cpp` to guarantee numerical stability, but a recent change to the build system broke it. 

Here are your instructions:
1. **Fix the Simulation Package**: Identify and fix the perturbation in `/app/fastsim-2.0.0` that is breaking the reproducible Kahan summation (hint: check the compiler flags). Recompile the package.
2. **Generate Data**: Run the compiled executable `./bin/generate_data 500 > /home/user/dataset.csv`. The output will be CSV formatted with columns `x` and `y`.
3. **Statistical Analysis**: Calculate the analytical Ordinary Least Squares (OLS) slope (regressing `y` on `x`). Then, calculate the 95% Bootstrap Confidence Interval for this slope. You must use exactly 2000 bootstrap resamples (sampling with replacement) and use a random seed of `42` for your bootstrap routine. You can write a Python script for this analysis step.
4. **Data Service**: Start an HTTP server listening on `127.0.0.1:8000`. It must expose a `GET /metrics` endpoint that returns a JSON response with the following exact keys:
   - `"analytical_slope"`: (float) the exact OLS slope calculated from the dataset.
   - `"bootstrap_ci_lower"`: (float) the 2.5th percentile of the bootstrap slope distribution.
   - `"bootstrap_ci_upper"`: (float) the 97.5th percentile of the bootstrap slope distribution.

Leave the server running in the background so it can be queried.