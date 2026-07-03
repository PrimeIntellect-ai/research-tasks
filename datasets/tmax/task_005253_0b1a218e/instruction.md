You are an AI assistant helping a researcher organize and analyze a dataset of sensor readings using C. 

The researcher has collected a dataset located at `/home/user/sensor_data.csv` with a header row `X,Y`. Due to sensor glitches, the data contains missing values and extreme outliers. You need to write a fast C program to clean the data, train a simple linear regression model, and evaluate it.

Write a C program named `/home/user/process.c` that does the following:
1. Opens and reads `/home/user/sensor_data.csv`.
2. Handles missing values: Discard any row where either `X` or `Y` is exactly the string `"NA"` or empty.
3. Handles outliers: Discard any row where the numerical value of `X` or `Y` is strictly less than `-1000.0` or strictly greater than `1000.0`.
4. Trains a simple linear regression model ($Y = mX + c$) on the cleaned dataset using the Ordinary Least Squares (OLS) method.
5. Evaluates the model by calculating the Mean Squared Error (MSE) over the *cleaned* training data.
6. Writes the results to `/home/user/results.log` in the exact following format (floating point numbers formatted to exactly 4 decimal places):

```
Slope: [m]
Intercept: [c]
MSE: [mse]
```

You are restricted to standard C libraries (`stdio.h`, `stdlib.h`, `string.h`, `math.h`, etc.). Compile your code using `gcc -O3 -o /home/user/process /home/user/process.c -lm` and run it to produce the `results.log` file.