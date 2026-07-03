You are a data engineer tasked with building a high-performance C++ ETL pipeline component for processing raw sensor data. 

You need to write a C++ program that processes a dataset located at `/home/user/sensor_data.csv`. The dataset has a header row and 3 numerical columns: `temp`, `pressure`, and `humidity`. 

Your C++ program (`/home/user/etl.cpp`) must perform the following pipeline steps in order:

1. **Missing Value Handling**: Read the CSV. Some values are missing (represented as empty strings `, ,` or `NaN`). Replace these missing values with the mean of the respective column. When calculating the mean, ignore the missing values.
2. **Outlier Handling**: For each column, calculate the mean ($\mu$) and the population standard deviation ($\sigma$). Cap the values in each column to be within $[\mu - 2\sigma, \mu + 2\sigma]$. If a value is less than $\mu - 2\sigma$, set it to $\mu - 2\sigma$. If it is greater than $\mu + 2\sigma$, set it to $\mu + 2\sigma$. (Calculate $\mu$ and $\sigma$ *after* missing value imputation).
3. **Feature Engineering**: Create a 4th column named `temp_pressure_interaction`, which is the element-wise product of the capped `temp` and `pressure` columns.
4. **Standardization**: Standardize all 4 columns (subtract the mean and divide by the population standard deviation of each respective column). 
5. **Dimensionality Reduction Prep (Covariance)**: Calculate the $4 \times 4$ covariance matrix of the standardized dataset. Use the sample covariance formula (divide by $N-1$).

Requirements:
- Output the cleaned, engineered, and standardized dataset to `/home/user/processed_data.csv` (include headers: `temp,pressure,humidity,temp_pressure_interaction`). Output values to 4 decimal places.
- Output the $4 \times 4$ covariance matrix to `/home/user/cov_matrix.txt`. Each row of the matrix should be on a new line, with values separated by spaces, formatted to 4 decimal places.
- You may download and use header-only libraries like Eigen if it helps you, but standard C++ is sufficient. 
- Compile your code into an executable at `/home/user/etl_bin` and run it to produce the output files.