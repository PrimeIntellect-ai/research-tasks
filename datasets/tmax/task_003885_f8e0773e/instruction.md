You are an AI assistant helping a researcher run simulations. The researcher has a physical model defined by a system of non-linear equations, and they need to find model parameters `(a, b)` such that the simulated outputs match a target empirical probability distribution as closely as possible.

Your task is to write a Python script at `/home/user/fit_distribution.py` that does the following:

1. **Non-linear Equation Solving**:
   For any given parameters `a` and `b`, the system state `y` (an array of 5 variables $y_0, y_1, y_2, y_3, y_4$) is the root of the following non-linear equations:
   $y_i - a \cdot \sin(y_{(i+1) \mod 5}) - b \cdot \cos(y_{(i-1) \mod 5}) - \frac{i}{10} = 0 \quad \text{for } i \in \{0, 1, 2, 3, 4\}$
   Use `scipy.optimize.root` (we recommend the `lm` method as the default Jacobian can be near-singular) with an initial guess of all zeros to find `y`.

2. **Probability Distribution**:
   Convert the solved state `y` into a probability distribution `p` over the 5 states using the softmax function: $p_i = \frac{e^{y_i}}{\sum_j e^{y_j}}$.

3. **Optimization and Distance Metric**:
   Find the optimal parameters `(a, b)` that minimize the 1D Wasserstein distance between the simulated distribution `p` and the target distribution `q = [0.1, 0.2, 0.3, 0.2, 0.2]`. 
   Assume the support (values) for both distributions is the array `[0, 1, 2, 3, 4]`.
   Use `scipy.stats.wasserstein_distance` to compute the distance.
   Use `scipy.optimize.minimize` (e.g., Nelder-Mead or L-BFGS-B) to find the best `(a, b)` starting from the initial guess `a=0.0, b=0.0`. Bound the parameters $a, b \in [-2, 2]$.

4. **Output**:
   The script must save the optimal parameters rounded to 3 decimal places to the file `/home/user/result.txt` in the format:
   `a,b`
   (For example: `0.123,-0.456`).

Write the script and run it to produce the `result.txt` file.