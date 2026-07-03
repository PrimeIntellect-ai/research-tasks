You are tasked with fixing a mathematical simulation pipeline for analyzing DNA sequence interactions and their impact on population dynamics. 

First, we have a vendored package located at `/app/adaptive_solve`. This package contains an adaptive ODE solver for the logistic equation `dy/dt = r*y - y^2`. However, the package currently crashes or diverges because the step-size adaptation logic is broken. Specifically, in its error control step, the ratio of tolerance to error has been inverted, causing the step size to decrease when the error is small and increase when the error is large. 
1. Fix the bug in `/app/adaptive_solve`. The correct adaptation formula used by the solver should be: `h_new = h_old * (tol / err)**0.5`. Ensure you install the package in your environment after fixing it.

Second, write a Python script at `/home/user/solve.py` that takes an arbitrary number of DNA sequences (strings containing A, C, G, T) as command-line arguments. The script must perform the following:
1. Compute an $N \times N$ matrix $A$, where $N$ is the number of input sequences, and $A_{i,j}$ is the length of the Longest Common Subsequence (LCS) between the $i$-th sequence and the $j$-th sequence.
2. Perform a Singular Value Decomposition (SVD) on the matrix $A$.
3. Extract the largest singular value, $\sigma_1$.
4. Use the fixed `adaptive_solve.integrator.integrate_logistic(r, y0=0.5, t_end=10.0, tol=1e-5)` function, passing $r = \sigma_1$ as the growth rate parameter.
5. Print the final result and the number of integration steps taken to standard output exactly in this format:
   `y_final: {y:.6f}, steps: {steps}`

Your script must be robust and produce deterministic output. Standard Python libraries and `numpy` are permitted.