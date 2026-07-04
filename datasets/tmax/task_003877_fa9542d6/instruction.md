You are an AI data scientist. We have a data pipeline that processes user activity, but our legacy scoring engine is a compiled, stripped binary without source code, and it runs too slowly to process our massive new datasets sequentially. 

Your task is to write a high-performance C++ program that performs data joining, aggregation, and scoring. 

Here are the details:
1. **Datasets**: 
   - `/home/user/demographics.csv`: Contains `uid`, `age` (int), `location_code` (int). (1 million rows)
   - `/home/user/activity.csv`: Contains `uid`, `clicks` (int), `impressions` (int), `duration_sec` (float). (Can have multiple rows per `uid`).

2. **The Oracle Binary**: 
   - Located at `/app/score_activity`.
   - Usage: `/app/score_activity <age> <location_code> <total_clicks> <total_impressions> <total_duration_sec>`
   - Outputs a single floating-point number (the "Activity Score") to standard output.
   - Calling this binary sequentially for 1 million users takes over an hour. You must find a way to process the data much faster in your C++ program (either by reverse-engineering the mathematical formula it uses via black-box probing, or by implementing an extremely efficient parallel execution wrapper). 

3. **Data Processing Requirements**:
   - Aggregate `activity.csv` so that for each `uid`, you compute the sum of `clicks`, `impressions`, and `duration_sec`.
   - Join this aggregated data with `demographics.csv` on `uid`.
   - Compute the Activity Score for each user based on their demographics and their *aggregated* total activity.
   - If a user in `demographics.csv` has no activity in `activity.csv`, their total clicks, impressions, and duration are all 0.

4. **Output**:
   - Write the final results to `/home/user/final_scores.csv`.
   - The file must have a header: `uid,score`.
   - The rows must be sorted by `uid` in ascending order.
   - The `score` should be formatted to 4 decimal places.

5. **Tooling**:
   - You must write your primary implementation in C++ (e.g., `/home/user/pipeline.cpp`).
   - You may use bash/Python to explore the data, probe the binary, install dependencies (e.g., `sudo apt-get install build-essential`), or prototype.

Your final output will be evaluated using a Mean Squared Error (MSE) metric against the true scores. You need an MSE of less than `0.001` to pass. Good luck!