You are acting as a Machine Learning Engineer preparing baseline training data for a Physics-Informed Neural Network (PINN). Due to strict container constraints in this specific environment, you must build a reproducible data generation pipeline using standard Linux utilities (Bash, Awk, standard shell tools) rather than Python.

Your task is to numerically solve a radioactive decay Ordinary Differential Equation (ODE), compare it to the analytical solution, test its convergence, and package the results into a dataset.

The ODE is:
dy/dt = -k * y

With parameters:
- k = 0.2
- Initial condition y(0) = 1000
- Time domain: t = 0 to t = 20

The analytical (exact) solution is: y(t) = y(0) * e^(-k*t)

Step 1: Write an ODE Solver
Create a script at `/home/user/ode_solver.sh` that takes a single command-line argument: the time step size `dt`.
Using the Forward Euler method, the script must calculate the numerical solution from t=0 to t=20.
The script must print the results to standard output in CSV format with the exact header:
`t,y_num,y_exact,abs_error`
(Where `abs_error` is the absolute difference between `y_num` and `y_exact`). 
Make sure the script is executable.

Step 2: Create the Data Pipeline
Write a master pipeline script at `/home/user/pipeline.sh` that does the following:
1. Creates a directory `/home/user/data/` if it doesn't exist.
2. Runs `ode_solver.sh` for the following `dt` values: `2.0`, `1.0`, `0.5`, `0.1`, `0.01`.
3. Saves the output of each run to `/home/user/data/dataset_dt_<dt>.csv` (e.g., `dataset_dt_2.0.csv`).
4. Extracts the final absolute error (the `abs_error` at exactly t=20) from each run and logs it to `/home/user/convergence_log.txt`.

The format for `/home/user/convergence_log.txt` must be:
```
dt,final_abs_error
2.0,<error_value>
1.0,<error_value>
0.5,<error_value>
0.1,<error_value>
0.01,<error_value>
```

Run your pipeline so that the dataset and convergence log are fully generated.