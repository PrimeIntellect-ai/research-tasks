You are an ML Engineer preparing training data for a material classification model based on spectroscopy signals. The raw sensor data is noisy and suffers from a known temperature-dependent background drift. You need to build a reproducible data processing pipeline in Go.

Your tasks are as follows:

1. **Environment Setup**: 
   Create a Go project in `/home/user/ml_pipeline`. Initialize a Go module (name it `ml_pipeline`) and add the `gonum.org/v1/gonum` package, which you will use for matrix operations.

2. **Data Ingestion**:
   A raw dataset is located at `/home/user/raw_spectra.csv`. It contains 10 rows (samples) and 100 columns (time steps from $t=0.0$ to $t=9.9$, with $\Delta t=0.1$).

3. **Background Subtraction (ODE Solving)**:
   The background interference follows a known cooling curve modeled by the ODE:
   $dy/dt = -0.1 \cdot y$
   
   With the initial condition $y(0) = 50.0$.
   Write Go code to numerically integrate this ODE from $t=0.0$ to $t=9.9$ using the **Forward Euler method** with a step size of $\Delta t = 0.1$.
   Subtract this computed background vector $y$ from *every row* of the raw spectra to get the corrected signal matrix $M$ (size 10x100).

4. **Dimensionality Reduction (Matrix Decomposition)**:
   Using the `gonum` library, perform a Singular Value Decomposition (SVD) on the corrected matrix $M$. 
   Extract the largest (first) singular value from the decomposition.

5. **Output**:
   Write this single largest singular value to a file at `/home/user/svd_result.txt`, formatted as a float with exactly 4 decimal places (e.g., `123.4567`).

Write the complete Go code in `/home/user/ml_pipeline/process.go`, build it, and run it to produce the output file.