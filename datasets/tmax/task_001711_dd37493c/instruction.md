You are an AI assistant helping a researcher run a numerical simulation involving optimization. 

The researcher has written a Go script located at `/home/user/test_stability.go` that performs gradient descent to find the local minimum of a simulation energy function $f(x) = x^4 - 3x^3 + 2$. 

Currently, the script is numerically unstable. Due to the high learning rate (`0.1`) and the steepness of the function, the gradient explodes, causing the values to diverge rapidly and resulting in `NaN` or `+Inf` values.

Your task is to:
1. Fix the numerical stability issue in `/home/user/test_stability.go` by implementing **gradient clipping**. Specifically, before applying the gradient to update `x`, clip the gradient value so it never exceeds `5.0` and never falls below `-5.0`.
2. Do not change the initial start value (`x = 4.0`), the learning rate (`0.1`), or the number of iterations (`1000`).
3. Run the modified Go script.
4. After running, take the final converged value of `x`, round it to exactly 2 decimal places (e.g., `1.23`), and write this single floating-point number to a new file at `/home/user/solution.txt`.

Ensure your Go code compiles and runs successfully. The final answer should be written strictly as a single number in the text file.