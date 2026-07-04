You are assisting a researcher who is running simulations on molecular network graphs. 
There are three CSV files representing weighted adjacency matrices of different molecular graphs in the directory `/home/user/matrices`. 

Your task is to:
1. Create a Python virtual environment at `/home/user/venv` and install `numpy` and `scipy`.
2. Analyze the three matrices (`graph_A.csv`, `graph_B.csv`, `graph_C.csv`). Compute the matrix rank of each using SVD-based methods (e.g., `numpy.linalg.matrix_rank`).
3. Identify the matrix with the highest rank and the matrix with the lowest rank.
4. For these two specific matrices, compute the node degree for each node (the sum of the weights in each row).
5. Perform an independent two-sample t-test comparing the node degrees of the highest rank matrix (Group 1) against the lowest rank matrix (Group 2) using `scipy.stats.ttest_ind` with default parameters.
6. Write your final results to a log file at `/home/user/result.log` using exactly the following format:

```
Highest: [filename]
Lowest: [filename]
T-stat: [value rounded to 2 decimal places]
P-value: [value rounded to 4 decimal places]
```

Example of expected output format in `/home/user/result.log`:
```
Highest: graph_Z.csv
Lowest: graph_X.csv
T-stat: 1.23
P-value: 0.2345
```