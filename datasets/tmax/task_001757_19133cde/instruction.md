You are a data scientist cleaning a raw dataset of 2D sensor readings. 
The dataset is located at `/home/user/sensor_data.csv`. It contains two columns, `X` and `Y`, separated by a comma (no header row).

Some of the sensor readings are corrupted. A corrupted reading is indicated by a missing value (encoded as `-999.0`) or extreme outliers caused by hardware glitches.

Your task is to write a C program that processes this data, cleans it, and computes specific statistical and regression metrics.

Here are the requirements:
1. Write a C program in `/home/user/process.c`.
2. The program must read `/home/user/sensor_data.csv`.
3. Filter out the corrupted rows: Any row where `X` OR `Y` is strictly less than `-50.0` or strictly greater than `50.0` must be completely ignored.
4. For the remaining valid data points, calculate the following:
   - The number of valid data points (N).
   - The mean of X and the mean of Y.
   - The sample covariance matrix: `Cov(X,X)`, `Cov(Y,Y)`, and `Cov(X,Y)`. (Make sure to use the unbiased estimator, i.e., divide by N-1).
   - The Simple Linear Regression coefficients to predict Y from X (i.e., Y = mX + c). Find the slope (`m`) and y-intercept (`c`).
5. Your C program must output these calculated values to a file named `/home/user/clean_stats.txt` in the exact format shown below, with all floating-point numbers formatted to exactly 4 decimal places (using `%.4f`).

Required Output Format for `/home/user/clean_stats.txt`:
```
Valid Count: [integer]
Mean X: [float]
Mean Y: [float]
Cov(X,X): [float]
Cov(Y,Y): [float]
Cov(X,Y): [float]
Slope (m): [float]
Intercept (c): [float]
```

You should write, compile, and execute this C program. Ensure the output file is correctly generated before considering the task complete.