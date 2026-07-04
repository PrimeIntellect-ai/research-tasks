You are acting as a data scientist working on fitting long-tailed data to a Pareto (Type I) distribution. Your task is to write a C program to compute the Maximum Likelihood Estimation (MLE) of the Pareto distribution parameters, validate it against an analytical reference case via a regression test, and then apply it to a new dataset.

The Pareto (Type I) distribution has two parameters:
- Scale parameter ($x_m$): The minimum possible value of $X$.
- Shape parameter ($\alpha$): The tail index.

The analytical MLE formulas for a dataset $X$ of size $N$ are:
1. $x_m = \min(X_i)$
2. $\alpha = \frac{N}{\sum_{i=1}^N \ln(X_i / x_m)}$

Here are your instructions:

1. Create a C program at `/home/user/src/pareto_fit.c` that takes a single command-line argument (the path to a dataset text file containing one positive float per line). The program should read the floats, calculate $x_m$ and $\alpha$ using the MLE formulas, and print the result to standard output in exactly this format: `xm: %.3f, alpha: %.3f\n`.

2. Write a bash regression test script at `/home/user/src/regression.sh`. This script must:
   - Compile the C program (producing the executable `/home/user/src/pareto_fit`). Link the math library (`-lm`) if needed.
   - Run the executable on `/home/user/data/test_data.txt`.
   - Validate that the output matches the analytically derived expectation for this specific test set. (The expected $x_m$ is 2.000, and you must calculate the exact expected $\alpha$ for the test set values: 2.0, 2.5, 3.0, 4.0, 5.0, then assert the C program outputs it correctly). The script should exit with code 0 if successful, and non-zero if it fails.

3. After your regression test passes, run your compiled `pareto_fit` program on the target dataset located at `/home/user/data/target_data.txt`.

4. Save the final estimated parameters for the target dataset into a JSON file at `/home/user/fit_results.json`. The file must contain exactly one JSON object with the keys "xm" and "alpha", and their respective values rounded to exactly 3 decimal places. Example: `{"xm": 1.234, "alpha": 5.678}`.

Assume `gcc` and standard C libraries are already installed on the system.