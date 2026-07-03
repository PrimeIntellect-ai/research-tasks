As a performance engineer, you are profiling a new matrix factorization tool. The tool frequently fails on near-singular inputs due to numerical instability. You have generated a profiling log located at `/home/user/profiling_data.csv` with the following columns:
`MatrixID,ConditionNumber,FactorizationTime_ms,Status`

Your task is to analyze this log using standard Bash utilities (like `awk`, `grep`, `sort`, etc.) to understand the tool's behavior. 

Please perform the following steps:
1. Identify the two matrices with the highest `ConditionNumber` that still successfully completed (i.e., their `Status` is `SUCCESS`).
2. Calculate the linear slope of the execution time as a function of the condition number for these two matrices.
   Formula: `slope = (Time2 - Time1) / (Cond2 - Cond1)`
   Save the calculated slope (as a floating-point number, e.g., using standard `awk` output format) to `/home/user/slope.txt`.
3. Extract the `MatrixID` of all runs that resulted in a `FAILED` status AND had a `ConditionNumber` strictly greater than `1.0e+12`. 
   Save these `MatrixID`s to `/home/user/unstable_matrices.txt`, with one ID per line, sorted numerically in ascending order.

You must only use Bash and standard Linux command-line tools (no Python, Perl, etc.).