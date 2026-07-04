You are assisting a researcher who is organizing and analyzing sensor datasets. The researcher needs a fast C++ tool to clean a small dataset and perform basic dimensionality reduction.

The dataset is located at `/home/user/dataset.csv`. It contains 3 columns of numerical data representing 3D coordinates.

Your task is to write a C++ program (e.g., `process.cpp`) that performs the following steps:
1. **Outlier Handling**: Read the CSV file. Any value strictly greater than 100.0 or strictly less than -100.0 is a sensor error and must be treated as a missing value (NaN). The CSV also contains explicit "NaN" strings.
2. **Missing Value Imputation**: For each column, calculate the arithmetic mean of the valid (non-NaN, non-outlier) values. Replace all missing values/outliers in that column with this mean.
3. **Data Centering**: Subtract the column mean from every value in that column so the column has a mean of 0.
4. **Covariance & PCA**: Compute the sample covariance matrix (divide by N-1, where N is the number of rows). Compute the eigenvalues and eigenvectors of this covariance matrix. 
5. **Output**: Find the principal component (the eigenvector corresponding to the largest eigenvalue). To resolve sign ambiguity, if the first component (X) of this eigenvector is negative, multiply the entire eigenvector by -1. Write the 3 components (X, Y, Z) of this principal eigenvector to `/home/user/top_pc.txt`, separated by commas, formatted to exactly 4 decimal places.

**Environment & Constraints:**
* You must use C++ and the Eigen3 library for linear algebra.
* You do not have root access to install packages via `apt`. You must download the Eigen headers locally into `/home/user/eigen` (e.g., from `https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.gz`) and compile your code including that directory (`-I/home/user/eigen/eigen-3.4.0`).
* Compile and run your program to generate `/home/user/top_pc.txt`.