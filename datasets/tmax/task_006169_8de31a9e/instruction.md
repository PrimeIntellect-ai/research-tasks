You are an AI assistant helping a data scientist clean a dataset of embeddings.

The dataset is located at `/home/user/embeddings.csv`. It contains 1000 rows and 5 columns (features/dimensions) of floating-point values representing embeddings. There is no header row. The data scientist suspects that some dimensions are highly redundant.

Your task is to identify the pair of distinct dimensions that have the highest absolute Pearson correlation coefficient. This is a crucial step before applying dimensionality reduction techniques.

You must do this by writing a C program and a reproducible shell pipeline. 

Specific Requirements:
1. Write a C program named `/home/user/find_correlation.c` that:
   - Reads the `/home/user/embeddings.csv` file.
   - Computes the covariance and then the Pearson correlation matrix for the 5 dimensions.
   - Finds the pair of distinct dimensions (0-indexed) with the highest absolute correlation.
   - Prints the result to standard output in the exact format: `idx1,idx2,correlation` where `idx1 < idx2` and `correlation` is formatted to exactly 4 decimal places (e.g., `1,3,-0.8421`).

2. Create a bash script named `/home/user/pipeline.sh` that:
   - Compiles the C program using `gcc` (make sure to link the math library).
   - Runs the compiled program.
   - Saves the standard output of the C program to exactly `/home/user/highest_correlation.txt`.

Ensure `/home/user/pipeline.sh` is executable and works correctly when run from `/home/user/`.