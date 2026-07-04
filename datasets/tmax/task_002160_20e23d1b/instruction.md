You are a bioinformatics analyst studying an idealized model of DNA unwinding energy along a synthetic chromosome.

We have generated a sequence energy profile stored in `/home/user/energy_signal.csv`. The file contains two columns: `x` (normalized genomic position from 0 to 10, with a step size of 0.01) and `E` (the modeled unwinding energy at that position). 

The theoretical energy is analytically defined by the continuous function:
E(x) = x * cos(x) + sin(x)

Your task is to write a C++ program that numerically analyzes this signal, validates it against the analytical solution, and outputs the results.

1. Write a C++ program in `/home/user/analyze.cpp` that reads `/home/user/energy_signal.csv`.
2. Compute the numerical integral of the energy signal over the entire domain [0, 10] using the **Trapezoidal Rule**.
3. Compute the maximum absolute numerical derivative (rate of change) of the energy signal across the domain using the **Central Difference Method** (you may ignore the first and last points where central difference cannot be applied).
4. Calculate the analytical integral of E(x) from x=0 to x=10 (you will need to derive the integral of E(x) mathematically to evaluate this).
5. Calculate the absolute error between your numerical integral and the analytical integral.
6. Compile your program using `g++` and run it.
7. Write the results to `/home/user/analysis_output.txt` exactly in the following format, rounding all numerical values to exactly 4 decimal places (e.g., using `std::fixed` and `std::setprecision(4)`):

```
Numerical Integral: [value]
Analytical Integral: [value]
Integral Error: [value]
Max Derivative: [value]
```

Please complete the task by leaving the correctly formatted `/home/user/analysis_output.txt` file in the home directory.