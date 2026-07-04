You are a data engineer building a high-performance C++ ETL pipeline for IoT sensor data. The downstream machine learning models require clean, low-dimensional data. You need to write a C++ program that reads raw sensor data, handles missing values and outliers, and performs Dimensionality Reduction (PCA).

Here are your instructions:

1. **Environment Setup**: 
   Since you do not have root access, download the Eigen3 library source code locally to `/home/user/eigen` to use for matrix operations. You can download it via:
   `wget https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.gz` and extract it.

2. **Input Data**: 
   Assume there is an input CSV file at `/home/user/raw_sensors.csv`. It contains 5 numerical columns (comma-separated, no header). Some values are missing and represented as `NaN`.

3. **Data Cleaning (C++ Implementation)**:
   Write a C++ program `/home/user/etl_pipeline.cpp` that performs the following steps in order:
   - **Missing Value Imputation**: Replace any `NaN` in a column with the mean of the *valid* (non-NaN) values in that same column.
   - **Outlier Capping**: After imputation, calculate the standard deviation ($\sigma$) and mean ($\mu$) of each column. Cap values in each column to the range $[\mu - 2\sigma, \mu + 2\sigma]$. If a value is less than $\mu - 2\sigma$, set it to $\mu - 2\sigma$. If it's greater than $\mu + 2\sigma$, set it to $\mu + 2\sigma$. Use population standard deviation (divide by N, not N-1).

4. **Dimensionality Reduction (PCA)**:
   - Mean-center the cleaned data (subtract the column mean from each feature).
   - Compute the covariance matrix.
   - Perform eigendecomposition using Eigen3.
   - Project the mean-centered data onto the top 2 principal components (the eigenvectors corresponding to the 2 largest eigenvalues).

5. **Output**:
   - Write the resulting 2D dataset to `/home/user/processed_data.csv`.
   - The file should be comma-separated, with 6 decimal places of precision.

6. **Compilation and Execution**:
   Compile your code using `g++` (e.g., `g++ -I /home/user/eigen/eigen-3.4.0 -O3 etl_pipeline.cpp -o etl_pipeline`) and run it to produce the output.