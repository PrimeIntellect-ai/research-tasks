You are a data scientist tasked with cleaning and optimizing a high-dimensional sensor dataset using a custom C-based pipeline. The raw data is located at `/home/user/sensor_data.csv`. It contains 200 rows. Each row has 120 continuous features followed by an integer class label (0 or 1) in the last column, all separated by commas.

Because standard tools are too slow for the production environment, you need to build this pipeline primarily in **C**, orchestrated by Bash.

Your objective is to perform dimensionality reduction via "feature binning", tune the bin size hyperparameter using Leave-One-Out Cross-Validation (LOOCV), and output the final cleaned dataset.

Here are the exact requirements:

1. **Write a C program (`/home/user/pipeline.c`)**:
   - It should accept an integer hyperparameter `k` (the bin size) as a command-line argument.
   - **ETL & Dimensionality Reduction**: The program must read `sensor_data.csv`. It should reduce the 120 features by averaging non-overlapping blocks of `k` adjacent features. For example, if `k=4`, features 1-4 are averaged into a new feature 1, features 5-8 into feature 2, and so on, resulting in 30 new features. The label remains unchanged. Assume `k` will always perfectly divide 120.
   - **Cross-Validation**: Implement 1-Nearest Neighbor (1-NN) Leave-One-Out Cross-Validation using standard Euclidean distance on the newly reduced feature space. 
   - **Output**: The C program should output the LOOCV accuracy (as a percentage or fraction) to stdout, or provide a way for a bash script to read this accuracy. It should also have a mode or a separate execution path to output the transformed dataset to a file.

2. **Write an orchestration script (`/home/user/run.sh`)**:
   - This bash script should compile `pipeline.c` using `gcc`.
   - It should perform **Hyperparameter Tuning** by executing the compiled C program over the following candidate values for `k`: `2, 3, 4, 5, 6, 8, 10, 12, 15, 20`.
   - It must determine which `k` produces the highest LOOCV 1-NN accuracy. **Tie-breaker:** If multiple values of `k` yield the same maximum accuracy, choose the *largest* `k` (which results in the most dimensionality reduction).
   - Finally, it must write the best `k` value to `/home/user/best_k.txt` (just the integer) and save the corresponding reduced dataset to `/home/user/cleaned_data.csv`.

**Formatting Rules for `cleaned_data.csv`**:
- Comma-separated values.
- Float features must be printed to exactly 4 decimal places (e.g., `%.4f`).
- The last column must be the integer label.
- The row order must exactly match the input `sensor_data.csv`.

Ensure your scripts are fully executable (`chmod +x /home/user/run.sh`) and self-contained. The automated test will run `/home/user/run.sh` and then verify the contents of `/home/user/best_k.txt` and `/home/user/cleaned_data.csv`.