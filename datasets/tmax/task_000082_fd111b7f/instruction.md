You are a data scientist attempting to fit an implicit, non-linear physical model to a reference dataset. 

The relationship between the independent variable $x$ and the dependent variable $y$ is governed by the following implicit equation:
$$y^3 + p_1 y - p_2 x = 0$$

You have a dataset of observed $(x, y_{obs})$ pairs. Your goal is to write a C++ program that finds the optimal parameters $p_1$ and $p_2$ that minimize the Sum of Squared Errors (SSE) between the predicted $y_{pred}$ and the observed $y_{obs}$.

$$SSE = \sum_{i} (y_{pred, i} - y_{obs, i})^2$$

Write a C++ program at `/home/user/fit_model.cpp` that performs the following steps strictly:

1. **Read the Reference Dataset:**
   Parse the dataset located at `/home/user/dataset.csv`. The file has a header `x,y_obs` and comma-separated float values.

2. **Nonlinear Equation Solving:**
   Implement the Newton-Raphson method to solve for $y_{pred}$ given $x$, $p_1$, and $p_2$.
   - Initial guess for $y$: `1.0`
   - Maximum iterations: `50`
   - Convergence tolerance: Stop when $|f(y)| < 10^{-6}$

3. **Optimization:**
   Implement Gradient Descent to optimize $p_1$ and $p_2$.
   - Initial parameters: $p_1 = 1.0$, $p_2 = 1.0$
   - Number of iterations: `1000`
   - Learning rate ($\eta$): `0.005`
   - Compute the gradients of the SSE with respect to $p_1$ and $p_2$ using the **central finite difference method** with step size $h = 10^{-4}$. 
     *(e.g., $\frac{\partial SSE}{\partial p_1} \approx \frac{SSE(p_1+h, p_2) - SSE(p_1-h, p_2)}{2h}$)*
   - Update rule: $p_k \leftarrow p_k - \eta \frac{\partial SSE}{\partial p_k}$

4. **Output Verification:**
   After the 1000th iteration, output the final optimized parameters and the final SSE to a JSON file at `/home/user/results.json`. The JSON must exactly match this format:
   ```json
   {
     "p1": 1.2345,
     "p2": 1.2345,
     "sse": 0.0012
   }
   ```
   (Round the values to 4 decimal places).

Compile your code using `g++ -O3 -std=c++17 /home/user/fit_model.cpp -o /home/user/fit_model` and execute it to produce the `results.json` file.