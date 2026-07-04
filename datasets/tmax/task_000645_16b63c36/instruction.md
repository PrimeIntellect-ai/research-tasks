I am a bioinformatics analyst working with fluorescence spectroscopy data. I have time-series data tracking a protein folding intermediate in `/home/user/data/spectroscopy.csv`. The data contains two columns: `time` and `signal`.

We model this process as an irreversible two-step reaction: State A -> State B -> State C, where the fluorescence signal is directly proportional to the concentration of State B. The initial conditions at t=0 are A=1.0, B=0.0, C=0.0.

I am trying to use our in-house Python package `bio_kinetics` (located at `/app/bio_kinetics`) to simulate this model and fit the rate constants $k_1$ (for A->B) and $k_2$ (for B->C) to my data. The package provides a function `simulate_B(k1, k2, t_eval)` which is supposed to return the concentration of B at the given time points.

However, the custom numerical integrator inside the package diverges and produces NaNs because of a suspected bug in its step-size adaptation logic. 

Your task is to:
1. Identify and fix the step-size adaptation bug in the `bio_kinetics` package so that it integrates stably and efficiently.
2. Install the package in the environment.
3. Write a Python script to fit the parameters $k_1$ and $k_2$ to the experimental data in `/home/user/data/spectroscopy.csv`. Use an initial guess of $k_1=1.0, k_2=1.0$.
4. Save the optimized parameters to `/home/user/fitted_params.csv`. The file must contain exactly one line with the two values separated by a comma: `k1,k2`.

The automated verifier will read your `fitted_params.csv` and compute the Mean Squared Error (MSE) between your fitted model's signal and the provided experimental data. To succeed, the MSE must be less than 0.005.