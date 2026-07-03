You are acting as a bioinformatics analyst. We have a set of DNA sequences and a matrix of positional weights, and we need to predict the binding affinity of a new target protein. 

Historically, our simulation engine produced non-reproducible aggregate binding scores across different compute nodes because the positional scores were being summed in non-deterministic orders (due to multi-threading), leading to floating-point drift. To establish a reproducible baseline and compare it to our empirical laboratory reference data, you must write a script to process the data according to very strict reduction rules, and then fit a model to the reference dataset.

You may use any programming language of your choice (e.g., Python, R, Bash tools).

**Data Files Provided:**
All files will be located in `/home/user/data/` (you should assume they exist when you start).
1. `weights.csv`: A single-column CSV containing 80 floating-point values. These represent a flattened 4x20 weight matrix (4 rows, 20 columns) in row-major order. Row 0 corresponds to 'A', Row 1 to 'C', Row 2 to 'G', and Row 3 to 'T'. Columns 0 to 19 correspond to the position in the sequence.
2. `sequences.txt`: 100 DNA sequences, each exactly 20 characters long, containing only A, C, G, and T.
3. `gold_standard.txt`: 100 floating point values, representing the empirically measured laboratory binding affinities for the corresponding sequences in `sequences.txt`.

**Your Task:**
1. Reshape the `weights.csv` into a 2D array (4 rows by 20 columns).
2. For each sequence in `sequences.txt`, extract the appropriate weight for each of its 20 positions. (e.g., if the first character is 'C', the weight is at row 1, column 0).
3. **Crucial floating-point stability step**: To strictly simulate our deterministic baseline reduction order, you MUST sort the 20 extracted positional weights for a sequence in strictly **ascending numeric order** before summing them together. Sum these sorted weights using standard 64-bit floats to compute the "Raw Score" for the sequence.
4. Perform a linear regression (Curve fitting) using the calculated Raw Scores as the independent variable (X) and the values in `gold_standard.txt` as the dependent variable (Y). Model: $Y = \text{Slope} \times X + \text{Intercept}$.
5. Calculate the Mean Squared Error (MSE) of this linear fit.
6. Write the final regression statistics to `/home/user/results/regression_stats.txt` in the exact format shown below, with values rounded to 4 decimal places.

**Required Output Format (`/home/user/results/regression_stats.txt`):**
```
Slope: <value>
Intercept: <value>
MSE: <value>
```

**Constraints:**
- You must create the `/home/user/results/` directory if it does not exist.
- Rely on standard CLI tools or basic standard numerical libraries (like `numpy` or `scipy` if using Python) to do the array manipulation and regression.