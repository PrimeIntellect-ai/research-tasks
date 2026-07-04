You are a data scientist working on an industrial monitoring dataset. We have a raw video feed from a factory camera, but the sensor occasionally glitches, producing corrupted (completely black) frames. Your goal is to clean this dataset, extract visual features, and build a local similarity search API in Go.

Here are the specific requirements:

1. **Video Processing**:
   - You are provided with a video file at `/app/factory_feed.mp4`.
   - Use `ffmpeg` to extract all frames from this video at 1 fps (frames per second) as JPEG images into `/home/user/frames/`. Name them sequentially as `frame_0001.jpg`, `frame_0002.jpg`, etc.

2. **Data Cleaning (Outlier Handling)**:
   - Some extracted frames are corrupted (black frames resulting from sensor dropouts). 
   - Write a Go script to calculate the average grayscale pixel intensity of each frame.
   - Any frame with an average pixel intensity of less than 5.0 (on a 0-255 scale) should be considered an outlier/missing value. Delete these corrupted frame files from the `/home/user/frames/` directory.
   - Log the filenames of the deleted corrupted frames into `/home/user/corrupted_frames.log`, one per line.

3. **Feature Extraction and Storage**:
   - For the remaining valid frames, compute a normalized 8-bin grayscale histogram.
   - Store the mapping of `filename` to its `8-bin histogram` (an array of 8 float64 values) in a SQLite database at `/home/user/features.db` in a table named `frame_features` (columns: `filename TEXT PRIMARY KEY`, `bin0 REAL`, ..., `bin7 REAL`).

4. **Similarity Search Service**:
   - Write and run a Go web service that listens on `127.0.0.1:8080`.
   - The service must expose an endpoint: `POST /search`.
   - It should accept a JSON payload: `{"target_frame": "frame_0010.jpg", "top_k": 3, "token": "data-sci-auth-77"}`.
   - It must validate the `token` (rejecting requests with HTTP 401 if it doesn't match "data-sci-auth-77").
   - It should retrieve the histogram for `target_frame` from SQLite, compute the Euclidean distance against all other valid frames in the database, and return a JSON response containing the `top_k` most similar frames (excluding the target itself): `{"results": ["frame_0015.jpg", "frame_0003.jpg", "frame_0022.jpg"]}`.

Start the web service in the background and ensure it is fully operational.