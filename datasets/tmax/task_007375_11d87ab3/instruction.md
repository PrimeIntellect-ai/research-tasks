You are an AI assistant helping a computational biology researcher. The researcher is studying the population dynamics of a bacterial strain and needs to fit a logistic growth model to their observational data.

The logistic growth ODE is given by:
dP/dt = r * P * (1 - P / K)
where `P` is the population, `r` is the growth rate, and `K` is the carrying capacity.

You need to implement the numerical solver and evaluation metric in C, and orchestrate the parameter sweep using a Jupyter Notebook.

Here are your specific tasks:

1. **Write the numerical solver in C:**
   - Create a C program at `/home/user/simulate.c`.
   - The program should take three command-line arguments: the path to a CSV data file, the growth rate `r` (float), and the carrying capacity `K` (float).
   - Usage: `./simulate <csv_path> <r> <K>`
   - The CSV file (`/home/user/population_data.csv` - already present on the system) contains two columns: `t` (time, integer) and `P` (observed population, float), with a header row.
   - The program must parse the CSV to get the initial population `P0` at `t=0`.
   - It must use the Runge-Kutta 4th Order (RK4) method to numerically solve the ODE from `t=0` to the maximum `t` found in the CSV. Use a fixed time step of `dt = 0.1`.
   - Compute the Sum of Squared Errors (SSE) between the simulated population and the observed population *only at the time points present in the CSV*. (Assume the CSV time points are integers, so your RK4 steps of 0.1 will align perfectly with them every 10 steps).
   - Print *only* the final SSE value to standard output as a floating-point number.

2. **Orchestrate the parameter sweep via Jupyter Notebook:**
   - Create a Jupyter Notebook at `/home/user/workflow.ipynb`.
   - The notebook should contain Python code to:
     a. Compile the C program to an executable named `simulate` in the same directory using `gcc`.
     b. Iterate over a grid of parameters: `r` in `[0.1, 0.2, 0.3]` and `K` in `[300.0, 400.0, 500.0]`.
     c. For each combination, execute the C program using the `subprocess` module, passing `/home/user/population_data.csv`.
     d. Capture the SSE output.
     e. Identify the `r` and `K` combination that produces the minimum SSE.
     f. Save the best parameters to a JSON file at `/home/user/best_fit.json` with exactly this format:
        `{"best_r": 0.2, "best_K": 400.0, "min_sse": 1.2345}`
        (Keep the SSE value raw as parsed from the C output, don't worry about rounding).

3. **Execute the workflow:**
   - Run the notebook headlessly to generate the final JSON file. You can use `jupyter nbconvert --to notebook --execute /home/user/workflow.ipynb`.

Ensure all file paths are exact and your C program strictly outputs just the numeric SSE to make it easily parseable by your notebook.