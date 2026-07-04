You are a data analyst working with an embedded systems team. We have a large batch of sensor data in a CSV file, and we need a highly efficient C++ pipeline to process this data, train a simple linear regression model, and evaluate its accuracy. 

Your task is to build a reproducible C++ ETL and modeling pipeline.

1. There is a dataset located at `/home/user/data/sensors.csv`. It has three columns: `id`, `temperature`, and `pressure`. The first row is the header.
2. Write a C++ program at `/home/user/process_data.cpp` that reads this CSV file.
3. The program should treat `temperature` as the independent variable (X) and `pressure` as the dependent variable (Y).
4. Train a simple Ordinary Least Squares (OLS) linear regression model to find the slope (m) and intercept (c) for the line `Y = mX + c`.
5. Evaluate the model by calculating the Mean Squared Error (MSE) over the same dataset.
6. The C++ program must write exactly three lines to a file at `/home/user/output/model_metrics.txt` in the following format (rounding values to exactly 4 decimal places):
   ```
   Slope: <m>
   Intercept: <c>
   MSE: <mse>
   ```
7. Create a bash script at `/home/user/run_pipeline.sh` that compiles the C++ program using `g++ -O3 -std=c++17 -o process_data process_data.cpp` and then executes `./process_data`. 

Make sure `/home/user/run_pipeline.sh` is executable. You should execute your pipeline script to generate the final `model_metrics.txt` file.