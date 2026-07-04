You are tasked with processing a video artifact and joining its data with a large historical dataset to find correlated events.

We have a video file located at `/app/experiment.mp4`. 
We also have a large historical CSV file at `/app/history.csv` containing past event logs with the following columns: `event_id`, `timestamp`, `intensity`, `category`, `location_id`.

Your objectives:
1. **Video Processing:** Extract the mean pixel intensity for every frame of `/app/experiment.mp4`. Convert each frame to grayscale, calculate the mean pixel value, and round it to the nearest integer. Save this data as `/home/user/frames.csv` with columns: `frame_number` (starting at 0) and `mean_intensity`.
2. **Database Construction:** Create a SQLite database at `/home/user/data.db`. Load both `/home/user/frames.csv` and `/app/history.csv` into this database into tables named `frames` and `history` respectively.
3. **Query Implementation:** Write a Python script `/home/user/fast_query.py` that connects to `/home/user/data.db` and performs the following query:
   - Find all records in the `history` table where the `intensity` matches the `mean_intensity` of ANY frame extracted from the video.
   - Filter the results to only include records where `category` is either 'A' or 'C'.
   - Order the results by `timestamp` descending, then by `event_id` ascending.
   - Implement pagination: retrieve exactly the 2nd page of results, assuming a page size of 50 (i.e., skip the first 50 results and return the next 50).
   - The script should print ONLY the `event_id` of the resulting records to standard output, one per line.
4. **Performance Optimization:** The dataset in `history.csv` is large (millions of rows). Your query must execute extremely fast. Design and apply appropriate index strategies in your SQLite database before running the query.

**Verification:**
An automated test will run your script as `python3 /home/user/fast_query.py`.
It will be evaluated on two criteria:
1. **Accuracy:** The output must exactly match the expected list of `event_id`s.
2. **Performance:** The script must finish execution in under 0.25 seconds.

Feel free to use `sqlite3`, `pandas`, `cv2` (OpenCV), or any other standard Python libraries available. Do not use external database servers; use standard local SQLite. Ensure your database indexes are created permanently in `/home/user/data.db` before the final script is tested.