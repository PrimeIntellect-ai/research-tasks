You are a data engineer building a high-performance ETL pipeline. As part of a new data ingestion step, we need a lightweight, ultra-fast C++ utility to perform real-time feature selection and basic model training on incoming micro-batches of sensor data. 

There is a dataset located at `/home/user/sensor_data.csv`. The file is a comma-separated values (CSV) file containing a header row followed by numeric data. The columns are `F1`, `F2`, `F3`, `F4`, and a target variable `T`.

Your task is to write a C++ program at `/home/user/pipeline.cpp` that does the following using ONLY the C++ Standard Library (no external ML libraries like Eigen or mlpack):

1. **Parse the CSV Data**: Read `/home/user/sensor_data.csv`.
2. **Correlation Analysis**: Compute the Pearson correlation coefficient between each feature (`F1`, `F2`, `F3`, `F4`) and the target `T`. 
3. **Feature Selection**: Identify the single feature that has the highest absolute correlation with the target `T`.
4. **Model Training**: Train a simple univariate linear regression model (`T = w * F_selected + b`) using the Ordinary Least Squares (OLS) method on the selected feature.
5. **Output**: Write the results to `/home/user/etl_model_output.txt` with exactly the following format (ensure floating-point numbers are rounded/formatted to exactly 4 decimal places):

```
SelectedFeature: [FeatureName]
Correlation: [PearsonCorrelationValue]
Weight: [w]
Bias: [b]
```

**Requirements:**
- The source file must be at `/home/user/pipeline.cpp`.
- Compile it to `/home/user/pipeline` (e.g., using `g++ -O3 -std=c++17 /home/user/pipeline.cpp -o /home/user/pipeline`).
- Execute the compiled binary to generate `/home/user/etl_model_output.txt`.
- Do not use external libraries (e.g., Boost, Eigen). Standard C++ libraries (`<iostream>`, `<fstream>`, `<vector>`, `<cmath>`, `<numeric>`, etc.) are required.