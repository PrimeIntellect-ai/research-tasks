You are a data scientist tasked with cleaning a dataset using C. 

You have been given two CSV files containing measurements from a sensor network:
1. `/home/user/data_X.csv`: Contains two columns `ID` (integer) and `X` (float).
2. `/home/user/data_Y.csv`: Contains two columns `ID` (integer) and `Y` (float).

The files might not be in the exact same order, but they contain the same set of IDs.

Your task is to write a C program located at `/home/user/processor.c` that does the following:
1. **Multi-source data joining**: Read both CSV files and join the data on the `ID` column.
2. **Correlation and covariance analysis**: Compute the Pearson correlation coefficient ($r$) between `X` and `Y` across the joined dataset.
3. **Regression and Anomaly Detection (Cleaning)**: Fit a Simple Linear Regression model ($Y = mX + c$) using Ordinary Least Squares. Identify all "clean" data points where the absolute residual $|Y_i - (mX_i + c)|$ is strictly less than `1.5`.

Your program must output the results as follows:
- Write the Pearson correlation coefficient to `/home/user/correlation.txt`, formatted to exactly four decimal places (e.g., `0.9123`).
- Write the filtered "clean" data to `/home/user/cleaned.csv`. Include a header row `ID,X,Y`. Sort the output by `ID` in ascending order. Format the floats `X` and `Y` to four decimal places.

**Constraints & Notes:**
- You must write the solution entirely in C. Standard C libraries (`stdio.h`, `stdlib.h`, `math.h`, `string.h`) are sufficient.
- Compile your program using `gcc /home/user/processor.c -lm -o /home/user/processor`.
- Assume there are exactly 100 rows of data. 
- You may use standard Linux commands to inspect the data and compile/run your code.