You are an AI assistant helping a materials researcher analyze spectral data from a chemical sensor network.

The researcher has deployed a network of sensors. Each sensor records a linear spectral response (Absorbance vs. Wavelength). However, due to data volume, they only want to perform regression analysis on the "most central" sensor—defined as the sensor with the highest degree centrality (most connections) in the network. If there is a tie, pick the lowest Node ID.

Your task is to write a C program that performs this analysis using graph algorithms, curve fitting, and matrix decomposition.

Here is the step-by-step workflow you must implement:
1. Ensure the GNU Scientific Library (GSL) is installed on the system (you may need to install `libgsl-dev`).
2. Write a C program at `/home/user/sensor_analysis.c`.
3. The program must read `/home/user/network.txt`, which contains the unweighted, undirected adjacency matrix of the sensor network (space-separated integers). Row/column indices correspond to Node IDs (0-indexed). Find the Node ID with the highest degree centrality.
4. The program must read `/home/user/spectra.csv`. This file has a header `NodeID,Wavelength,Absorbance`. Extract all the `Wavelength` (x) and `Absorbance` (y) data points corresponding ONLY to the selected Node ID.
5. Perform linear regression ($y = \beta_0 + \beta_1 x$) on this node's spectral data. To do this, you **must** formulate the normal equations $X^T X \beta = X^T y$, where $X$ is the design matrix (first column is 1s, second column is Wavelengths) and $y$ is the Absorbance vector.
6. Solve for $\beta$ by performing a Cholesky decomposition on the symmetric positive-definite matrix $X^T X$ using GSL (`gsl_linalg_cholesky_decomp` and `gsl_linalg_cholesky_solve`).
7. Write the resulting parameters to `/home/user/solution.txt` in the exact following format (values rounded to exactly 4 decimal places):
```
Node: <ID>
Intercept: <beta_0>
Slope: <beta_1>
```

Compile your C program using:
`gcc -o /home/user/sensor_analysis /home/user/sensor_analysis.c -lgsl -lgslcblas -lm`

Execute the program and ensure `/home/user/solution.txt` is created with the correct data.