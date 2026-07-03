You are a machine learning engineer preparing training data. You need to calculate the 95% bootstrap confidence interval for the mean of a target variable in an observational dataset. However, previous attempts yielded non-reproducible results due to random seeding and floating-point accumulation differences. You must implement a strictly reproducible Monte Carlo bootstrap simulation using standard Linux tools (Bash, coreutils, `awk`).

Your task is to write a bash script at `/home/user/bootstrap.sh` that does the following:

1. Reads the dataset `/home/user/data.csv`. The file is comma-separated. The first line is the header (`id,feature1,feature2,target`).
2. Extracts the `target` column (the 4th column), ignoring the header.
3. Uses `awk` to perform 1000 bootstrap iterations to compute the distribution of the mean. 
   - To guarantee exact reproducibility, you MUST use `awk` and initialize the random number generator exactly once in the `BEGIN` block using `srand(42)`.
   - Read the extracted target values into a 1-indexed array `val`.
   - In the `END` block, run an outer loop 1000 times (for the bootstrap iterations).
   - Inside the outer loop, initialize a sum to 0, and run an inner loop $N$ times (where $N$ is the total number of data rows).
   - In the inner loop, select a random index using `idx = int(rand() * N) + 1` and add `val[idx]` to your sum.
   - After the inner loop, print the sample mean (`sum / N`) formatted to 6 decimal places (`%.6f`).
4. Sort the 1000 output means in ascending numerical order and save them to `/home/user/means.txt`.
5. Extract the 95% confidence interval boundaries. Specifically, take the 25th value (2.5th percentile) and the 975th value (97.5th percentile) from the sorted list (1-indexed).
6. Save these two values comma-separated to `/home/user/ci.txt` in the format `lower,upper` rounded to 4 decimal places (e.g., `5.1234,6.7890`).

You must only use bash built-ins and standard coreutils (like `awk`, `sort`, `sed`, `tail`, `head`, `printf`, etc.). Do not use Python, R, or any other programming languages.

Execute your script to ensure `/home/user/means.txt` and `/home/user/ci.txt` are generated correctly.