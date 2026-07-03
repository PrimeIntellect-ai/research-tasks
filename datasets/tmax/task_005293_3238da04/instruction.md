You are acting as a performance engineer profiling a hybrid C++/Python numerical application. 

In `/home/user/integrator.cpp`, there is a C++ implementation of an adaptive Heun-Euler (Order 2/1) numerical integrator. It is designed to solve the simple decay ODE $y' = -\lambda y$. However, it suffers from a numerical instability and performance issue: it frequently diverges or hits the maximum step limit because the step-size adaptation logic contains a critical mathematical error.

Your tasks are to:
1. Identify and fix the step-size adaptation bug in `/home/user/integrator.cpp`. The step size $h$ should scale proportionally to $\sqrt{\text{tol} / \text{error}}$, but the current implementation has an error in this formula.
2. Compile the fixed C++ code into a shared library at `/home/user/libintegrator.so`. Use `g++ -shared -fPIC -O2`.
3. Write a Python regression testing script at `/home/user/run_analysis.py` that uses the `ctypes` module to load the compiled library and interface with the `integrate` function.
4. Using your Python script, run the integrator for $\lambda = 5.0$, starting from $y(0) = 1.0$ at $t = 0.0$ to $t_{\text{end}} = 2.0$.
5. Run this integration for three different tolerance levels: `1e-2`, `1e-3`, and `1e-4`.
6. For each tolerance, extract the number of steps taken and the absolute error of the final value compared to the analytical ground-truth solution ($y(t) = e^{-\lambda t}$).
7. Save the results to `/home/user/analysis.json` exactly in this format:
```json
{
  "1e-2": {
    "steps": 123,
    "error": 0.00123
  },
  "1e-3": {
    "steps": 456,
    "error": 0.00012
  },
  "1e-4": {
    "steps": 789,
    "error": 0.00001
  }
}
```

Make sure your C++ compilation step is successful and your Python script runs without errors to produce the correct JSON.