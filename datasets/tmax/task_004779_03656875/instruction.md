You are an AI assistant helping a computational chemistry researcher automate a data analysis workflow. The researcher has simulated the rate of product formation in a chemical reaction over time, but needs you to integrate this rate to find the total product concentration, fit it to a kinetic model, and visualize the result. 

Because the lab uses a mix of Python and Gnuplot for historical reasons, you must build a multi-language workflow.

Here is what you need to do:

1. **Input Data**: You will find a file at `/home/user/reaction_rate.csv`. It has two comma-separated columns with a header: `Time,Rate`. 
2. **Numerical Integration and Curve Fitting (Python)**:
   Write a Python script at `/home/user/analyze.py` that:
   - Reads `/home/user/reaction_rate.csv`.
   - Numerically integrates the `Rate` with respect to `Time` using the Trapezoidal rule (e.g., `scipy.integrate.cumulative_trapezoid` or `numpy.trapz` cumulatively) to compute the cumulative product concentration, $C(t)$. Assume $C(0) = 0$.
   - Fits the integrated data to the first-order kinetic model: $C(t) = A \cdot (1 - \exp(-k \cdot t))$ to find parameters $A$ (maximum yield) and $k$ (rate constant).
   - Writes the fitted parameters $A$ and $k$ to `/home/user/fit_params.txt` in the format: `A=X.XXX, k=Y.YYY` (rounded to 3 decimal places).
   - Saves a new CSV file `/home/user/integrated_data.csv` with columns: `Time,Cumulative_C,Fitted_C`.
3. **Visualization (Gnuplot)**:
   Write a Gnuplot script at `/home/user/plot.gnu` that:
   - Sets the terminal to PNG.
   - Sets the output file to `/home/user/result_plot.png`.
   - Plots both `Cumulative_C` and `Fitted_C` from `/home/user/integrated_data.csv` against `Time` on the same graph. Use comma as the data separator.
4. **Workflow Orchestration (Bash)**:
   Write a bash script at `/home/user/run_workflow.sh` that:
   - Executes the Python script.
   - Executes the Gnuplot script.
   Make sure it has execute permissions.

You only need to create these three scripts (`analyze.py`, `plot.gnu`, `run_workflow.sh`) and then execute `/home/user/run_workflow.sh` to produce the final outputs.