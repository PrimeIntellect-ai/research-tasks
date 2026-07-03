You are a data engineer tasked with an unusual ETL pipeline. We have an optical tracking system that outputs its raw data as a video file, and a broken SQL pipeline that is supposed to process this data.

Your objectives:
1. **Data Extraction**: Analyze the video `/app/tracking.mp4`. The video contains a single bright white dot moving on a dark background. Write a script to extract the (X, Y) coordinates of the center of this bright dot for each frame (0-indexed).
2. **Database Load**: Create a SQLite database at `/home/user/tracking.db`. Create a table `positions(frame_id INTEGER, x REAL, y REAL)` and insert your extracted coordinates.
3. **Pipeline Fix**: We have a broken SQL script at `/home/user/etl.sql`. It is intended to calculate the Euclidean distance traveled since the *previous* frame, and then compute a 5-frame moving average of this distance (the current frame and the 4 preceding frames). The current script contains a cross-join that produces incorrect results and hangs on large datasets. 
4. **Data Querying & Export**: Rewrite the SQL query using proper window functions (e.g., `LAG`, `AVG(...) OVER (...)`) to calculate the `distance` and `moving_avg_distance`. Export the results to `/home/user/smoothed_speeds.csv` with columns: `frame_id`, `distance`, `moving_avg_distance`. 

Note: 
- For `frame_id = 0`, `distance` should be 0 or NULL, and `moving_avg_distance` will just be the average of available frames (which is just the 1st frame's distance).
- The CSV must have a header.

Your final output will be graded by the Mean Squared Error (MSE) of your `moving_avg_distance` values compared to the true trajectory.