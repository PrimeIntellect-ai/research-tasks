You are a data scientist modeling the local GC content sequence of a DNA fragment.

Write a Python script at `/home/user/fit_model.py` that performs the following steps:
1. Parse the FASTA file located at `/home/user/data.fasta` and extract the DNA sequence (ignore the header).
2. Calculate the GC fraction (count of 'G' and 'C' divided by window size) for consecutive, non-overlapping sliding windows of length 10. If the final window is shorter than 10 bases, discard it.
3. Fit an Auto-Regressive AR(1) model to these GC fractions: $y_t = \alpha y_{t-1} + \beta$, where $y_t$ is the GC fraction of the $t$-th window (0-indexed, $t$ ranges from 1 to $N-1$).
4. Use full-batch gradient descent to minimize the Mean Squared Error (MSE) over all valid transitions:
   $MSE = \frac{1}{N-1} \sum_{t=1}^{N-1} (y_t - (\alpha y_{t-1} + \beta))^2$
5. Gradient descent specifications:
   - Initialize $\alpha = 0.5$ and $\beta = 0.5$.
   - Use a constant learning rate $\eta = 0.1$.
   - **Numerical stability testing:** In each iteration, compute the gradients of the MSE with respect to $\alpha$ and $\beta$. Before updating the parameters, clip both gradients independently to the range $[-1.0, 1.0]$.
   - **Convergence testing:** Stop iterating when the absolute difference in MSE between the current iteration and the previous iteration is strictly less than $10^{-5}$, OR if you reach exactly 10,000 iterations. Compute the initial MSE before making any parameter updates to evaluate the difference after the first update.
6. Run your script. Have it write the final parameters and the number of iterations performed to `/home/user/result.csv` in the exact format:
   `alpha,beta,iterations`
   Round `alpha` and `beta` to 4 decimal places.

Do not write anything else to the output file. You may use standard Python libraries.