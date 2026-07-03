You are a data scientist tasked with fitting a linear model to a dataset using both optimization (Gradient Descent) and MCMC posterior evaluation techniques.

Your environment is a Linux terminal. All your coding must be done in C.

**Task details:**
1. Create a dataset file at `/home/user/dataset.csv` with the following exact content:
```csv
x,y
1.0,3.2
2.0,5.1
3.0,6.8
4.0,9.1
5.0,10.9
```

2. Write a C program at `/home/user/fit_model.c` that does the following:
   * **Part 1: Gradient Descent (Optimization)**
     Implement gradient descent to find the parameters `w` (weight) and `b` (bias) that minimize the Mean Squared Error (MSE) loss:
     `MSE = (1/N) * sum_{i=1}^N (y_i - (w*x_i + b))^2`
     * Set the initial values to `w = 0.0` and `b = 0.0`.
     * Use a learning rate of `0.02`.
     * Run for exactly `100` iterations.
     
   * **Part 2: MCMC Posterior Estimation (Log-Posterior Evaluation)**
     To prepare for an MCMC sampler, implement a function that computes the unnormalized log-posterior of the model given `w` and `b`.
     Assume uniform priors for `w` and `b`. 
     Assume the likelihood for each data point is a normal distribution centered at `w*x_i + b` with variance = 1.0.
     The unnormalized log-posterior is therefore equivalent to the log-likelihood:
     `LogPosterior = sum_{i=1}^N -0.5 * (y_i - (w*x_i + b))^2`
     (Omit the constant offset `-0.5 * ln(2*pi)` for this calculation).

3. The C program must output the final results after 100 iterations of Gradient Descent, and the LogPosterior evaluated at those final GD estimates. 

4. Compile your program and run it, saving its standard output to `/home/user/solution.txt`.

**Output Format Constraint:**
The output saved to `/home/user/solution.txt` must have exactly two lines formatted as follows (values rounded to 4 decimal places):
```
GD w: <w_val>, b: <b_val>
LogPosterior: <log_post_val>
```
Example (not real numbers):
```
GD w: 1.5032, b: 0.8124
LogPosterior: -1.2345
```