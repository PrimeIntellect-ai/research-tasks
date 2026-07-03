You are a Data Engineer building a high-performance, lightweight ETL (Extract, Transform, Load) pipeline in C for an embedded system. You need to join two data sources, perform dimensionality reduction, and run inference using a pre-trained logistic regression model.

You have been provided with two data files:
1. `/home/user/sensor_data_A.csv`: Contains columns `ID,F1,F2,F3`
2. `/home/user/sensor_data_B.csv`: Contains columns `ID,F4,F5,F6`

Your task is to write a C program at `/home/user/etl_pipeline.c`, compile it, and run it to produce `/home/user/predictions.csv`.

The pipeline must perform the following steps:
1. **Multi-source Data Joining**: Perform an inner join on `sensor_data_A.csv` and `sensor_data_B.csv` using the integer `ID` column. Only process IDs present in both files.

2. **Dimensionality Reduction**: Project the 6-dimensional feature vector $[F1, F2, F3, F4, F5, F6]$ down to a 2-dimensional vector $[Z1, Z2]$ using the following predefined projection matrix $P$:
   $$ P = \begin{bmatrix} 
   0.5 & -0.2 \\ 
   0.1 & 0.8 \\ 
   -0.3 & 0.4 \\ 
   0.9 & 0.1 \\ 
   0.0 & -0.5 \\ 
   0.2 & 0.3 
   \end{bmatrix} $$
   So, $Z1 = 0.5 \cdot F1 + 0.1 \cdot F2 - 0.3 \cdot F3 + 0.9 \cdot F4 + 0.0 \cdot F5 + 0.2 \cdot F6$, and similarly for $Z2$.

3. **Classification Inference**: Pass $[Z1, Z2]$ through a logistic regression model.
   - Weights: $W_1 = 1.5, W_2 = -2.0$
   - Bias: $b = 0.5$
   - Logit: $L = (W_1 \cdot Z1) + (W_2 \cdot Z2) + b$
   - Probability: $p = \frac{1}{1 + e^{-L}}$
   - Predicted Class: $1$ if $p \ge 0.5$, else $0$

**Output Requirements**:
Write the results to `/home/user/predictions.csv`.
The file must have a header: `ID,Probability,Class`
The `ID` should be formatted as an integer.
The `Probability` must be formatted to exactly 4 decimal places (e.g., `0.1234`).
The `Class` should be `0` or `1`.
Sort the output in ascending order by `ID`.

Note: You can use the standard C math library (`-lm`). You may use any standard Linux tools or install C libraries if necessary, but writing a self-contained C file using standard libraries is recommended.