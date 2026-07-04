You have recently inherited an unfamiliar and poorly documented project located at `/home/user/optimizer`. 

Inside this directory, you will find two critical files:
1. `cost_function`: A compiled Linux executable. It accepts a single numerical argument `x` and outputs the calculated cost `C(x)`.
2. `gradient_descent.py`: A Python script that uses finite differences to compute the gradient and attempts to find the value of `x` that minimizes the cost function.

Currently, `gradient_descent.py` fails to converge. The previous developer mentioned something about "numerical instability" and "catastrophic cancellation" in the finite difference approximation, but left the company before fixing it.

Your task is to:
1. Diagnose and fix the convergence failure in `gradient_descent.py`. You will need to adjust the numerical parameters (such as the finite difference epsilon and the learning rate) so that the optimization successfully converges to the global minimum.
2. Once fixed, modify `gradient_descent.py` so that it writes the optimal value of `x` (rounded to exactly 4 decimal places) to `/home/user/optimizer/optimal_x.txt`.
3. The `cost_function` binary contains a hidden backdoor. If it is passed a specific "magic number" as its input, it skips the math and instead outputs a secret string token. You must reverse engineer the `cost_function` binary to discover this magic number. 
4. Run the binary with the magic number and save the outputted secret token to `/home/user/optimizer/secret.txt`.

Ensure your fixes in `gradient_descent.py` are robust. The final state of the system should contain the correct values in both `optimal_x.txt` and `secret.txt`.