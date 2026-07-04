You are a machine learning engineer preparing synthetic training data. You are using a C program that numerically solves an ODE to generate a 10x10 feature covariance matrix.

However, the current C code (`/home/user/data_gen.c`) has a reproducibility and precision bug: it uses a naive floating-point summation inside the ODE integration loop. Due to floating-point accumulation errors when summing many small values into a growing accumulator, the results are drifting from the mathematically true values. 

Your task is to:
1. Modify `/home/user/data_gen.c` to replace the naive summation (`sum += y * dt;`) inside `compute_feature` with the **Kahan summation algorithm** (using `float` precision variables, strictly following the standard Kahan algorithm: `y_val = (y * dt) - c`, `t = sum + y_val`, `c = (t - sum) - y_val`, `sum = t`). Do not change the data types to `double`; you must fix the algorithmic reduction order issue using Kahan summation.
2. Compile and run the modified `data_gen.c`. It will output a 10x10 matrix to `/home/user/matrix.txt`.
3. Read `/home/user/matrix.txt` and perform a Singular Value Decomposition (SVD) on this matrix.
4. Extract the **largest singular value** (the principal component magnitude) and write it, rounded to exactly 4 decimal places, to a file named `/home/user/result.txt`.

You may use Bash, Python, or write additional C code to perform the SVD and formatting, but the ODE integration loop fix must be done in the provided C file.