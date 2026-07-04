You are a Machine Learning Engineer preparing a simple 1D dataset for a downstream model. You have two files representing paired feature sets: `/home/user/X.csv` (the input feature) and `/home/user/Y.csv` (the reference target). Your goal is to find the best linear transformation $Y_{pred} = w \cdot X + b$ that minimizes the Mean Squared Error (MSE) between $Y_{pred}$ and $Y$. 

Because this is a strict environment with no Python or specialized ML libraries installed, you must perform this using only standard Linux shell tools (Bash, `awk`, `bc`, etc.).

Perform the following steps:

1. **Gradient Descent Optimization**: Write an `awk` script located at `/home/user/gd.awk` that reads `X.csv` and `Y.csv` (you can paste them together using `paste`) and performs Gradient Descent to find `w` and `b`. 
   - Hyperparameters: Learning rate = 0.5, Epochs = 500, Initial $w=0$, Initial $b=0$.
   - Output the final values to `/home/user/gd_result.txt` strictly in the format: `w,b` (rounded to 4 decimal places).

2. **Analytical Solution Validation**: To validate the optimization, write a second `awk` script located at `/home/user/analytical.awk` that computes the exact analytical solution for Simple Linear Regression.
   - Formulas: $w = \frac{Cov(X,Y)}{Var(X)}$ and $b = \bar{Y} - w\bar{X}$.
   - Output the exact values to `/home/user/analytical_result.txt` strictly in the format: `w,b` (rounded to 4 decimal places).

3. **Regression Test**: Write a Bash script `/home/user/test.sh` that:
   - Runs the gradient descent and analytical `awk` scripts.
   - Compares the `w` and `b` values from both results.
   - If the absolute difference for *both* $w$ and $b$ is less than 0.01, write the string `PASS` to `/home/user/regression.log`. Otherwise, write `FAIL`.
   - Run the script so the log file is generated.