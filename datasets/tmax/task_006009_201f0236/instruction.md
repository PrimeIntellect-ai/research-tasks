You are assisting a computational chemistry researcher. We are modeling thermal diffusion across a discrete molecular network (represented as a graph). The simulation uses an Ordinary Differential Equation (ODE) solver written in C to compute the state of each node over time.

However, the simulation currently fails and produces `NaN` or `Inf` values. The researcher suspects that the numerical integrator diverges due to a flawed step-size adaptation logic in the Euler method.

Here is your task:
1. **Fix the Simulation:** Inspect and fix the C program located at `/home/user/diffusion.c`. The step-size (`dt`) currently uses a broken adaptive scheme that causes the simulation to blow up. Modify the code to remove the adaptive logic entirely and use a strictly constant step size of `dt = 0.01` throughout the integration loop. Leave all other mathematical logic (the graph Laplacian calculations) intact.
2. **Compile and Run:** Compile the fixed program into an executable named `diffusion_sim` and run it. The program expects two arguments: an input graph and an output file name. Run it using `/home/user/molecule_graph.txt` as the input graph, and save the output to `/home/user/sim_results.csv`. The output will contain two columns: `Time` and `SystemEnergy`.
3. **Curve Fitting:** The system's energy decays exponentially over time: $E(t) = E_0 e^{-\alpha t}$. Create a script (in C, Python, or bash/awk) to estimate the decay rate $\alpha$. You must do this by performing an Ordinary Least Squares (OLS) linear regression on $\ln(E(t))$ versus $t$. **Only use data points where $1.0 \le t \le 5.0$** (inclusive).
4. **Reference Comparison:** The file `/home/user/reference_data.csv` contains theoretical $\alpha$ values for various molecules. Look up the reference $\alpha$ for the molecule named `Mol_Beta`.
5. **Reporting:** Create a final report at `/home/user/report.txt` with exactly the following format (replace the brackets with your calculated floating point numbers, rounded to 4 decimal places):
```
Computed Alpha: [Your computed alpha]
Reference Alpha: [Value from reference file]
Difference: [Absolute difference between the two]
```

**Note:** Ensure your regression correctly calculates the slope of the log-transformed energy. Do not use external curve-fitting libraries (like `scipy.optimize` or `numpy.polyfit`)—you must implement or use the standard mathematical formula for OLS linear regression slope: $m = \frac{n(\sum xy) - (\sum x)(\sum y)}{n(\sum x^2) - (\sum x)^2}$. You may use basic math modules.