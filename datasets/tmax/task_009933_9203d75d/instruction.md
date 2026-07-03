You are acting as a systems data analyst tasked with predicting job execution times based on historical system metrics. You need to implement a custom K-Nearest Neighbors (KNN) regression and benchmark its inference time using Go.

You have been provided with two CSV files (which you must assume exist in your environment, though you may need to generate dummy ones if you wish to test your code):
1. `/home/user/historical_jobs.csv`
   Columns: `JobID,CPU_Cores,RAM_GB,Disk_IOps,Job_Duration`
2. `/home/user/queries.csv`
   Columns: `QueryID,CPU_Cores,RAM_GB,Disk_IOps`

Your objective is to write a Go program located at `/home/user/predictor.go` that does the following without using any external machine learning or math libraries (standard library only):

1. **Data Loading & Preprocessing:**
   - Read `historical_jobs.csv`.
   - Calculate the minimum and maximum values for `CPU_Cores`, `RAM_GB`, and `Disk_IOps` based *only* on this historical dataset.
   - Use these min and max values to Min-Max scale the features of both the historical data and the queries to a [0, 1] range. 
     Formula: `Scaled = (Value - Min) / (Max - Min)`
     *(Note: If Max == Min, the scaled value should be 0).*

2. **Similarity Search & Regression (KNN):**
   - For each query in `queries.csv`, find the `k=3` nearest neighbors in the scaled historical dataset using Euclidean distance.
   - Calculate the predicted `Job_Duration` by taking the arithmetic mean of the `Job_Duration` of these 3 nearest neighbors.

3. **Inference Performance Benchmarking:**
   - Measure the exact time it takes to perform the similarity search and regression for *all* queries (exclude file I/O and preprocessing/scaling from this measurement).
   - Write this inference duration in microseconds as a simple integer to a file named `/home/user/benchmark.txt`.

4. **Output Generation:**
   - Write the predictions to `/home/user/predictions.csv` with exactly two columns: `QueryID,Predicted_Duration`.
   - The `Predicted_Duration` should be formatted to exactly two decimal places (e.g., `42.50`).

Run your Go program to generate `/home/user/predictions.csv` and `/home/user/benchmark.txt`. Do not leave the files empty. Ensure your code is robust against standard CSV formatting (e.g., headers).