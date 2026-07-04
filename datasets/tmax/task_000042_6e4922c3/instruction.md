You are a data analyst working on a performance-critical data processing pipeline. You have a dataset of sensor readings, but to optimize downstream systems, you need to extract the most significant axis of variance (the first Principal Component) using a lightweight, dependency-free C program. 

Your task is to implement this dimensionality reduction tool from scratch.

A dataset has been provided at `/home/user/sensor_data.csv`. It contains 500 rows and 20 columns of comma-separated floating-point numbers (no header).

Write a C program at `/home/user/pca.c` that does the following:
1. **Read the Data:** Load the 500x20 matrix from `/home/user/sensor_data.csv`.
2. **Mean-Center:** Calculate the mean of each of the 20 columns and subtract it from every element in that column.
3. **Covariance Matrix:** Compute the 20x20 sample covariance matrix $C = \frac{1}{N-1} X_c^T X_c$, where $X_c$ is the mean-centered data matrix and $N=500$.
4. **Power Iteration:** Use the Power Iteration algorithm to find the dominant eigenvector (the first Principal Component) of the covariance matrix.
   - Initialize your eigenvector $v$ as a 20-element array where every element is exactly `1.0`.
   - Perform exactly `100` iterations of the algorithm ($v_{new} = C v$, followed by normalizing $v_{new}$ by its Euclidean ($L_2$) norm).
5. **Sign Determinism:** After 100 iterations, if the *first* element of the normalized eigenvector is negative, multiply the entire eigenvector by `-1.0`.
6. **Output:** Save the 20 elements of the final eigenvector to `/home/user/first_component.txt`. Write each float on a new line, formatted exactly to 6 decimal places (e.g., using `%.6f\n`).

You must compile your program using `gcc` (e.g., `gcc -O3 /home/user/pca.c -o /home/user/pca -lm`) and run it to produce the output file.