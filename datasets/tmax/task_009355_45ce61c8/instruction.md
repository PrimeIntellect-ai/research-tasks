You are a Machine Learning Engineer preparing to deploy a lightweight inference engine on an embedded system. You need to write a standalone C program to parse raw training data, perform inference for two pre-trained models (one regression, one classification) using basic linear algebra, and benchmark their combined execution performance.

Your tasks are:

1. **Write the Inference Engine (`/home/user/engine.c`)**:
   - Read the dataset from `/home/user/data.csv`. This file contains 10,000 rows, each with 3 comma-separated float features (`x0, x1, x2`).
   - Implement **Linear Regression**:
     - Weights: `W_lin = {0.5, 1.5, -0.5}`
     - Bias: `B_lin = 1.0`
     - Equation: $y = (W_{lin} \cdot X) + B_{lin}$
   - Implement **Logistic Regression** (Classification):
     - Weights: `W_log = {-1.0, 0.5, 2.0}`
     - Bias: `B_log = -0.5`
     - Equation: $p = \frac{1}{1 + e^{-z}}$ where $z = (W_{log} \cdot X) + B_{log}$
     - A row is classified as `1` (positive) if $p \ge 0.5$, else `0` (negative). Use standard `math.h` functions.

2. **Benchmark Inference Performance**:
   - Inside your C program, load the dataset into memory first (do not include I/O in the benchmark).
   - Record the wall-clock time.
   - Run a benchmark loop that computes the predictions for *both* models over all 10,000 rows, repeated exactly **10,000 times**.
   - Record the end wall-clock time and calculate the elapsed time in seconds.

3. **Output Results**:
   - After running the code, your program must write exactly three lines to `/home/user/output.txt`:
     - Line 1: `Linear Sum: <SUM>`, where `<SUM>` is the sum of all linear regression predictions across a *single* pass of the dataset, rounded to exactly 2 decimal places.
     - Line 2: `Logistic Positives: <COUNT>`, where `<COUNT>` is the total number of positive class predictions across a *single* pass.
     - Line 3: `Benchmark Time: <TIME>s`, where `<TIME>` is the duration of the 10,000 iterations in seconds (formatted to 4 decimal places).

Compile your code using standard tools (e.g., `gcc -O3 engine.c -lm -o engine`) and run it to produce `/home/user/output.txt`.