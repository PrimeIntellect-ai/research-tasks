You are a data engineer building a mathematical ETL pipeline. We need to process tabular numerical data, transform it into polynomial embeddings, aggregate it by group, and tune a hyperparameter using a simple grid search. 

Your task is to implement the core processing engine in C++ and a wrapper Bash script for hyperparameter tuning.

**Step 1: Create the C++ ETL Processor**
Write a C++ program at `/home/user/etl_processor.cpp` that does the following:
1. Takes a single command-line argument: an integer `p` (the polynomial power).
2. Reads a CSV file located at `/home/user/data.csv`. The CSV has no header and contains three columns: `id` (integer), `v1` (double), and `v2` (double).
3. For each row, computes the polynomial embedding: `e1 = v1^p` and `e2 = v2^p`.
4. Aggregates the embeddings by `id` by summing them. For each unique `id`, let the sums be `S1` and `S2`.
5. Computes a global score for the dataset, defined as the sum of the L2 norms of the aggregated vectors: `Score = sum_over_ids( sqrt(S1^2 + S2^2) )`.
6. Prints ONLY the final global score to standard output, formatted to exactly 4 decimal places.

Compile the C++ program to an executable named `/home/user/etl_processor` using standard `g++`.

**Step 2: Hyperparameter Tuning via Bash**
Write a Bash script at `/home/user/tune.sh` that:
1. Iterates over the hyperparameter `p` for the values: 1, 2, 3, 4, 5.
2. Runs the compiled `/home/user/etl_processor` for each value of `p`.
3. Determines which value of `p` produces a score closest to the target value of `150.0`. (Minimize the absolute difference `|Score - 150.0|`).
4. Writes the best `p` and its corresponding score to a file at `/home/user/best_param.txt` in the exact format: `p=<best_p>,score=<best_score>` (e.g., `p=2,score=142.1234`).

Ensure your scripts and C++ code handle basic errors (like file not found) gracefully, but focus primarily on correctness of the math and pipeline.

Once you have written and compiled everything, execute `/home/user/tune.sh` to generate the final output file.