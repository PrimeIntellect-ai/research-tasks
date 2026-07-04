You are a data scientist analyzing object tracking data from a physics experiment. We have a raw video recording of the experiment, but the object occasionally flickers out of existence or is occluded, requiring data cleaning and imputation.

Your task is to extract the object's trajectory, clean the data, store it, and expose it via a local API for our visualization dashboard.

Step 1: Feature Extraction
Read the video file located at `/app/experiment.mp4`. For every frame (0-indexed), identify the Y-coordinate (row index, where 0 is the top) of the brightest pixel. 
- If the maximum pixel intensity in a frame is strictly less than 100 (on a 0-255 scale), consider the object "missing" in that frame (treat its Y-coordinate as NaN).

Step 2: Imputation and Rolling Statistics
- Use linear interpolation to fill in the missing Y-coordinates.
- Compute a rolling average of the *imputed* Y-coordinates using a centered window of size 5 (i.e., the current frame, 2 frames before, and 2 frames after). For the edges where a full window isn't available, output null/NaN or leave them out of the final serving if you prefer, but the calculation must be a standard centered 5-frame rolling mean (e.g., using `pandas.Series.rolling(window=5, center=True).mean()`).

Step 3: Database Storage
Bulk insert the processed data into an SQLite database located at `/home/user/tracking.db`. Create a table named `trajectory` with the following schema:
- `frame` (INTEGER PRIMARY KEY)
- `y_imputed` (REAL)
- `y_rolling_avg` (REAL)

Step 4: API Serving
Create and start a local HTTP web server (e.g., using Flask, FastAPI, or standard library) listening on `127.0.0.1:8000`. 
The server must expose a GET endpoint at `/api/stats` that accepts a `frame` query parameter. 
When queried (e.g., `GET /api/stats?frame=10`), it should fetch the corresponding row from the SQLite database and return a JSON response exactly like:
`{"frame": 10, "y_imputed": 45.0, "y_rolling_avg": 46.2}`
If the frame does not exist, return a 404 status code.

Leave the web server running in the background so the automated verification system can query it.