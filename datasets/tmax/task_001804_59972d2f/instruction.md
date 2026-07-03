You are a data scientist debugging a numerical simulation pipeline. We are simulating the decay of a certain signal over time across a variety of initial observations. 

You have been provided with a Go program at `/home/user/simulate.go` and a dataset of initial signal amplitudes at `/home/user/initial_states.csv`. 

The Go program parses the CSV, runs a simple Euler method numerical integrator to solve the ODE describing the signal decay ($dy/dt = -k \cdot y$, where $k = 0.5$) from $t=0$ to $t=5.0$, and writes the resulting final amplitudes to `/home/user/final_states.txt`.

However, there is a problem: the numerical integrator is producing wildly inaccurate, oscillating results because the time step `dt` is set too large, causing the step-size adaptation to fail or diverge from the analytical truth.

Your task:
1. Identify and fix the step-size issue in `/home/user/simulate.go`. Change the `dt` variable to `0.001` to ensure numerical stability and accuracy.
2. Compile and run the fixed Go program to generate `/home/user/final_states.txt`.
3. The generated file `/home/user/final_states.txt` will contain one final amplitude per line, corresponding to the initial states. 
4. Calculate the average "attenuation factor" across all the simulations. The attenuation factor for a single simulation is defined as `final_amplitude / initial_amplitude`.
5. Write this single mean attenuation factor to the file `/home/user/mean_attenuation.txt`, rounded to exactly 4 decimal places (e.g., `0.1234`).

Note: You may use shell utilities (like `awk`, `paste`, etc.) or write a small script to compute the final mean attenuation factor.