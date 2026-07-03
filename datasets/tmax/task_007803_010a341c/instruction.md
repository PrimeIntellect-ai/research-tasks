You are a data scientist tasked with fitting a statistical model to a dataset using custom optimization routines in C. You have a set of observed values and suspect they are drawn from a Cauchy distribution. Since standard libraries for this specific routine are unavailable in your constrained environment, you must implement the Maximum Likelihood Estimation (MLE) from scratch using Gradient Descent.

Your tasks are:
1. Write a C program `/home/user/fit_cauchy.c`.
2. The program must read 1000 floating-point numbers from `/home/user/data.txt`.
3. Implement Gradient Descent to minimize the Mean Negative Log-Likelihood (MNLL) of the Cauchy distribution on this dataset to find the optimal location ($x_0$) and scale ($\gamma$).
   The Mean Negative Log-Likelihood function is defined as:
   `MNLL = ln(pi) + ln(gamma) + (1/N) * sum_{i=1}^N ln(1 + ((x_i - x0)/gamma)^2)`
   Where `N` is the number of data points. Use `pi = 3.14159265358979323846`.
4. Calculate the partial derivatives of the MNLL with respect to $x_0$ and $\gamma$.
5. Perform Gradient Descent with the following hyperparameters:
   - Initial $x_0 = 0.0$
   - Initial $\gamma = 1.0$
   - Learning rate $\alpha = 0.5$
   - Number of iterations = 500
   Update rule: `theta = theta - alpha * gradient` (Update $x_0$ and $\gamma$ simultaneously at each step).
6. After 500 iterations, save the final estimated parameters to `/home/user/params.txt` exactly in this format:
   `x0=%.4f, gamma=%.4f`
7. Read 500 floating-point numbers from a holdout reference dataset `/home/user/reference.txt`.
8. Compare the fitted distribution against this reference set by computing the MNLL of the reference dataset using your final fitted $x_0$ and $\gamma$. Save this evaluation metric to `/home/user/eval.txt` exactly in this format:
   `MNLL=%.4f`

Requirements:
- Ensure you compile your program using `gcc -O3 -lm fit_cauchy.c -o fit_cauchy`.
- Execute your program so that the output files are generated.
- All variables should be `double` precision floats.