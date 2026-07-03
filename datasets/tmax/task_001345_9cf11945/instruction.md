You are tasked with building a lightweight data processing and inference pipeline. 

You have been provided with two files in your home directory:
1. `/home/user/data.csv`: A dataset containing an `id` column and three feature columns (`f1`, `f2`, `f3`). Some of the feature values are missing (empty fields, causing implicit schema issues if read directly).
2. `/home/user/weights.txt`: A single line of three comma-separated floating-point numbers representing a projection vector (weights for `f1`, `f2`, and `f3`).

Your objective is to:
1. Use standard Linux shell commands to parse `/home/user/data.csv` and create a cleaned version where any missing feature value (empty field between commas) is replaced with `0.0`. Skip the header row.
2. Write a C program at `/home/user/infer.c` that reads the cleaned data. For each row, it should parse the `id` and the three features, apply the weights from `/home/user/weights.txt` by computing the dot product (a simple linear dimensionality reduction/inference step), and output the `id` and the final computed score.
3. Compile your C program to `/home/user/infer`.
4. Run the pipeline and save the final results to `/home/user/scores.csv`.

The output file `/home/user/scores.csv` must be formatted strictly as:
```
id,score
```
Where `score` is formatted to exactly one decimal place (e.g., `1,12.0`).

Ensure your C code accurately enforces the schema (reading one integer and three floats per line) and handles the linear algebra cleanly.