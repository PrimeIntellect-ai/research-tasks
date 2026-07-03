You are acting as a computational researcher analyzing synthetic radioactive decay data. We suspect that the substance under study is actually a mixture of two isotopes, rather than a single pure isotope. 

Your task is to generate the simulation data, fit two competing statistical models, ensure the optimization has converged properly, and perform a statistical hypothesis test to determine if the two-isotope model is significantly better.

Follow these exact steps:

1. **Compilation and Data Generation**:
   There is a C source file located at `/home/user/simulate_decay.c`. This program simulates the decay process.
   - Compile this C program using standard `gcc` to an executable named `/home/user/simulate_decay`. Include the math library (`-lm`).
   - Run the executable and redirect its standard output to `/home/user/data.csv`. The output is a CSV with two columns: `t` (time) and `y` (activity).

2. **Optimization and Convergence Testing**:
   Write a Python script (e.g., `/home/user/analyze.py`) that reads `/home/user/data.csv` and fits two models using non-linear least squares optimization:
   - **Model 0 (Null Hypothesis - Single Isotope):** $y = A e^{-\lambda t}$
   - **Model 1 (Alternative Hypothesis - Two Isotopes):** $y = A e^{-\lambda_1 t} + B e^{-\lambda_2 t}$
   
   *Note:* Fitting double exponential models is notoriously sensitive to initial parameter guesses. You must implement a convergence testing strategy (e.g., trying multiple initial starting points or using global optimization) to ensure you have found the true global minimum (the lowest Residual Sum of Squares, RSS) for Model 1. 

3. **Statistical Hypothesis Comparison**:
   Compare the two nested models using an F-test. 
   - Calculate the Residual Sum of Squares for Model 0 ($RSS_0$) and Model 1 ($RSS_1$).
   - Calculate the F-statistic. (Remember the degrees of freedom for Model 0 is $N-2$, and for Model 1 is $N-4$, where $N$ is the number of data points).
   - Calculate the p-value from the F-distribution.

4. **Output Logging**:
   Create a results file at `/home/user/stats_result.txt` containing exactly the following four lines (replace `<value>` with the computed numbers, rounded to 4 decimal places):
   ```
   Model 0 RSS: <value>
   Model 1 RSS: <value>
   F-statistic: <value>
   p-value: <value>
   ```