You are a data analyst working on a traffic monitoring system. We have a video of traffic footage located at `/app/traffic_camera.mp4`. 

Your goal is to build a C++ data processing and regression pipeline that predicts traffic density based on frame-level video statistics.

Phase 1: Feature Extraction
Use `ffmpeg` (or `ffprobe`) to extract the "scene change score" (or absolute difference) between consecutive frames in `/app/traffic_camera.mp4`. 
Format the output into a CSV file named `/home/user/frame_stats.csv` with two columns: `frame_index` and `diff_score`. Note that some frames in our camera system are periodically corrupted and will yield an empty or 'NaN' difference score. You must represent these dropped/corrupted frames as `NaN` in the `diff_score` column of your CSV.

Phase 2: C++ Pipeline & Modeling
Write a C++ program at `/home/user/pipeline.cpp` that does the following:
1. Reads `/home/user/frame_stats.csv`.
2. Cleans the data: You must carefully handle the `NaN` values. A common bug in our previous pipeline was that missing string values were silently cast to `0` or `0.0` during parsing, completely skewing our distributions. You must drop rows with `NaN` values, NOT convert them to 0.
3. Feature Engineering: Compute a rolling average of the `diff_score` over a window of 5 valid frames.
4. Statistical Modeling: Implement a simple linear regression model (trained from scratch in C++) to predict the rolling average of frame $N+5$ based on the rolling average of frame $N$. 
5. Cross-Validation: Split your valid data into the first 70% for training and the remaining 30% for validation.
6. Benchmarking: Your C++ code must track its own inference time for the validation set.

Phase 3: Output
Your compiled C++ program (`/home/user/pipeline`) must output a file called `/home/user/predictions.csv`. 
The file should contain the predictions for the validation set, with columns `frame_index`, `actual_target`, and `predicted_target`.

Success Criteria:
We will evaluate your `/home/user/predictions.csv` using a programmatic metric. 
- You must achieve a Mean Squared Error (MSE) of less than `0.05` on the validation set.
- The C++ program must execute the inference portion in under 50 milliseconds.

Compile your code with `g++ -O3 /home/user/pipeline.cpp -o /home/user/pipeline` and run it to produce the final `predictions.csv`.