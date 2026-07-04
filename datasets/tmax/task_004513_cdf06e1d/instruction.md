You are a data scientist working on cleaning a noisy sensor time-series dataset. You need to build a C++ data processing pipeline to align, smooth, and clean the dataset. 

A colleague left a sticky note with the required cleaning parameters, which has been scanned and saved at `/app/cleaning_params.png`.

Your task is to:
1. Extract the `WINDOW` (an integer) and `ALPHA` (a float) parameters from the image `/app/cleaning_params.png`. (You can use `tesseract` to read it).
2. Write a C++ program at `/home/user/cleaner.cpp` that processes the dataset located at `/app/noisy_sensor.csv`. The CSV has no header and two columns: `timestamp` (Unix epoch integer) and `value` (float). 
3. The C++ pipeline must perform the following operations:
   - **Timestamp Alignment:** The input timestamps are irregular. Create a strictly regular 1-second grid from the minimum timestamp to the maximum timestamp in the file. Fill missing values using forward-fill (use the most recent past value). For the very first timestamp, use its exact value.
   - **Parallel Rolling Mean:** Apply a centered rolling mean over the regularized values using the `WINDOW` size extracted from the image. Because the window is centered, for a given index `i`, the window spans `[i - WINDOW/2, i + WINDOW/2]` (using integer division). If the window extends beyond the array boundaries, only average the available elements within the bounds. Implement this rolling mean using parallel data processing (e.g., using `std::thread` or OpenMP to process chunks of the array concurrently).
   - **Exponential Smoothing:** Over the rolling-mean output, apply an Exponential Moving Average (EMA) sequentially using the `ALPHA` extracted from the image. 
     Formula: `EMA_0 = X_0` and `EMA_t = ALPHA * X_t + (1 - ALPHA) * EMA_{t-1}` for `t > 0`.
4. The C++ program must write the final processed time series to `/home/user/clean_data.csv` (Format: `timestamp,value`, with 4 decimal places for the value).
5. Add pipeline logging: The C++ program must write a log to `/home/user/pipeline.log` with lines indicating "STARTED" and "COMPLETED" for each major phase.

Compile your C++ program (e.g., using `g++ -O3 -pthread`) and run it to produce `/home/user/clean_data.csv`. 

Your output will be evaluated automatically against a perfectly implemented reference output by computing the Mean Squared Error (MSE). The MSE must be strictly less than 0.001.