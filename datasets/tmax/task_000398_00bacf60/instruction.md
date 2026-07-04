You are an ML Engineer preparing embedding data for a cross-validation retrieval task. You have a raw dataset of embeddings that contains missing values and outliers.

Write a C program at `/home/user/clean_and_search.c` to perform data cleaning, folding, and nearest-neighbor retrieval.

**Dataset:**
The file `/home/user/embeddings.csv` contains 100 rows and 5 columns of floating-point numbers, comma-separated. Missing values are represented by the string `NaN`.

**Requirements for the C program:**
1. **Missing Value Imputation**: Calculate the mean of each column (ignoring `NaN` values). Replace all `NaN` values with their respective column's mean.
2. **Outlier Capping**: Calculate the population standard deviation ($\sigma$) of each column (using the imputed data). Cap all values in the column to a minimum of $\mu - 2\sigma$ and a maximum of $\mu + 2\sigma$ (where $\mu$ is the column mean).
3. **K-Fold Split**: Accept an integer `K` as a command-line argument (e.g., `./clean_and_search 5`). Split the 100 rows into `K` contiguous, equal-sized folds. (For $K=5$, Fold 0 is rows 0-19, Fold 1 is rows 20-39, etc. You can assume 100 will always be cleanly divisible by $K$).
4. **Query Embedding**: Compute a "query embedding" vector by taking the element-wise average of all vectors in **Fold 0**.
5. **Retrieval**: For each subsequent fold (Fold 1 through Fold $K-1$), find the single nearest neighbor to the query embedding using Euclidean distance.
6. **Output**: Your program must print the absolute, original row indices (from 0 to 99) of the nearest neighbors found in each fold (from 1 to K-1), separated by a single comma and a space. Write this exact string to standard output AND save it to `/home/user/result.txt`.

Example output for K=5:
`24, 47, 62, 88`

Compile your program and run it with `K=5` to produce the final `/home/user/result.txt`.