You are an AI assistant helping a data researcher organize and analyze a dataset of sparse feature vectors. 

The researcher has a file located at `/home/user/vectors.csv`. The file contains an `id` column followed by several numerical feature columns (`f1`, `f2`, ..., `f10`). Because of some data collection errors, some rows contain missing values (represented as empty strings). 

When read naively by data processing libraries like pandas, these missing values often cause entire integer columns to be silently cast to floating-point numbers due to NaN introduction. The researcher needs you to perform exact integer arithmetic to avoid floating-point precision issues down the line.

Please complete the following steps:
1. Create a Python virtual environment at `/home/user/venv` and install `pandas` and `numpy`.
2. Write and execute a Python script that reads `/home/user/vectors.csv`.
3. Drop any rows that contain missing values (NaNs).
4. Ensure the remaining feature vectors are treated as exact integers.
5. Using linear algebra (dot products), find all pairs of `id`s whose feature vectors are exactly orthogonal (i.e., their dot product is exactly 0).
6. Save the orthogonal pairs to `/home/user/orthogonal_pairs.txt`. 

Formatting requirements for `/home/user/orthogonal_pairs.txt`:
- Each line should contain exactly one pair of `id`s, separated by a comma (e.g., `A,B`).
- Sort the two `id`s within each pair alphabetically (e.g., write `A,B` instead of `B,A`).
- Sort the entire list of pairs alphabetically by the first `id`, then by the second `id`.
- Do not include pairs of an `id` with itself.

You may use standard Linux shell commands and Python.