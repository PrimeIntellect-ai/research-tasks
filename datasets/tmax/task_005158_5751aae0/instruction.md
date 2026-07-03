You are a Machine Learning Engineer preparing synthetic training data for a statistical model. 

We have a legacy sensor whose operational parameters are trapped in a scanned document located at `/app/priors.png`. You must extract these parameters and build a highly accurate C++ data generator that performs sequential Bayesian inference to establish confidence intervals on the sensor's true state.

Your objective:
1. Extract the "Prior Mean", "Prior Variance", and "Sensor Variance" from `/app/priors.png`. You may use `tesseract` to read the image.
2. Implement a C++ program at `/home/user/simulator.cpp` and compile it to an executable named `/home/user/simulator`.
3. The executable must accept command line arguments:
   - `argv[1]`: An integer identifier / seed (can be ignored in the math, but must be accepted).
   - `argv[2]` to `argv[argc-1]`: A sequence of floating-point numbers representing individual sensor observations.
4. For the given sequence of observations, perform sequential Bayesian updating assuming Gaussian distributions. Start with the Prior Mean and Prior Variance from the image. For each observation, apply the Bayesian update using the fixed Sensor Variance from the image.
5. Calculate the 95% Confidence Interval (CI) of the final posterior distribution (use Z = 1.95996).
6. The program must print exactly four space-separated floating-point numbers to standard output, formatted to 6 decimal places:
   `[final_posterior_mean] [final_posterior_variance] [ci_lower_bound] [ci_upper_bound]`

The output must be strictly numerically accurate and will be tested extensively against an automated fuzzer with random sequences of observations. Ensure all calculations use double precision.