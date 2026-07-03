You are acting as a data analyst who needs to process a CSV dataset and perform a simple linear regression using C.

We have a dataset located at `/home/user/data.csv` with the following contents:
```csv
x,y
1.0,2.1
2.0,3.9
3.0,6.2
4.0,8.0
5.0,10.1
```

Your task is to write a C program at `/home/user/train_model.c` that uses the GNU Scientific Library (GSL) to compute the simple linear regression of `y` on `x`. The GSL development libraries (`libgsl-dev`) are already installed on the system.

The program must meet the following requirements:
1. It must accept exactly one command-line argument: an integer representing the "Run ID".
2. It must read the dataset from `/home/user/data.csv` (skip the header line).
3. It must use the `gsl_fit_linear` function from `<gsl/gsl_fit.h>` to compute the intercept (`c0`) and slope (`c1`).
4. It must create (or overwrite) a file at `/home/user/model_output.txt` containing exactly:
   `Intercept: <c0>, Slope: <c1>`
   where both numbers are formatted to 4 decimal places.
5. It must append the result to an experiment tracking log file at `/home/user/experiment_log.txt` in the following format:
   `Run <ID>: c0=<c0>, c1=<c1>`
   where both numbers are formatted to 4 decimal places.

After writing the code:
- Compile your program into an executable named `/home/user/train_model` using `gcc`. Be sure to link the GSL and math libraries appropriately.
- Execute your compiled program using the Run ID `1042`.

Ensure that the final output files are created in `/home/user/` and contain the correct formatted values based on the regression of the provided data.