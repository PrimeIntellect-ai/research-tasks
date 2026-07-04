You are assisting a researcher who needs to process experimental sensor data, build a simple baseline model, and evaluate its numerical accuracy. 

The researcher has provided two pipe-separated datasets:
1. `/home/user/train_data.txt`
2. `/home/user/test_data.txt`

Both files have the following header and format:
`ID|Sensor_A|Sensor_B|Target`

Your task is to write a self-contained C++ program named `/home/user/pipeline.cpp` that implements an end-to-end Extract, Transform, Load (ETL) pipeline, trains a baseline linear regression model, and evaluates its accuracy.

Specifically, your C++ program must:
1. **ETL Processing**: Read the data. Filter out and discard any row (from both train and test sets) where:
   - `Target` is exactly the string `NaN`.
   - `Sensor_A` has a negative value (`< 0`).
2. **Model Training**: Using the cleaned training data, calculate a univariate Ordinary Least Squares (OLS) linear regression to predict `Target` using *only* `Sensor_A` as the feature. The model equation is `Target = m * Sensor_A + b`. 
3. **Numerical Accuracy Testing**: Using the learned parameters `m` and `b`, predict the `Target` values for the *cleaned* test dataset. Compute the Mean Absolute Error (MAE) of these predictions.
4. **Output**: Write the calculated values to a file named `/home/user/model_results.txt` in the exact format shown below, with each numeric value rounded to exactly 4 decimal places:
```
m: <value>
b: <value>
MAE: <value>
```

You are restricted to standard C++ libraries (e.g., `<iostream>`, `<fstream>`, `<sstream>`, `<vector>`, `<string>`, `<cmath>`, `<iomanip>`). Do not use external machine learning or linear algebra libraries like Eigen.

Compile your code, run it, and ensure `/home/user/model_results.txt` is generated correctly.