You are an AI assistant helping a systems researcher organize and analyze dataset access metrics across a large-scale storage cluster. 

The researcher has written a C program to compute the 95% confidence intervals for data access latency (in milliseconds) across various storage nodes. These metrics are used for experiment tracking. However, the program currently outputs completely blank/zeroed-out margins of error (e.g., `Mean ± 0.000`) due to a bug in how it processes the data types and variances.

Your task:
1. Fix the buggy C program located at `/home/user/analyze_latency.c`. The program is supposed to read raw binary files (containing sequences of `double` precision floats representing access times), calculate the sample mean, and compute the 95% confidence interval using the formula: `Margin = 1.96 * sqrt(Variance / N)`.
2. Compile your fixed program.
3. Run the program on all storage node binary files located in `/home/user/storage_metadata/`. There are three files: `node_alpha.dat`, `node_beta.dat`, and `node_gamma.dat`.
4. The program must output the results to an experiment tracking log located exactly at `/home/user/experiment_tracking.csv`. 

The output CSV must contain exactly this header row and format (sorted alphabetically by node name):
```csv
Node,Mean,CI_Lower,CI_Upper
node_alpha,X.XXX,Y.YYY,Z.ZZZ
node_beta,...
node_gamma,...
```
(Format the numerical values to exactly 3 decimal places).

Please examine the source code, fix the arithmetic/typing bugs causing the "blank/zero" variance calculations, compile it, and generate the correct `experiment_tracking.csv`.