You are an AI assistant acting as a data scientist. We have a corrupted video feed dataset that needs to be cleaned and processed. 

There is a video file located at `/app/dirty_feed.mp4`. We need to extract the frames, identify the corrupted ones using specific feature extraction and distance metrics, and serve the cleaning results via an API.

Please complete the following workflow:

1. **Frame Extraction**:
   Use `ffmpeg` to extract all frames from `/app/dirty_feed.mp4` into the directory `/home/user/frames/`. Use the naming format `frame_%04d.jpg` and extract at exactly 10 frames per second (fps).

2. **Feature Extraction and Similarity Computation**:
   Write a Python pipeline (e.g., `pipeline.py`) that processes these frames in numerical order. For each frame, compute:
   - **Brightness Feature**: The average pixel intensity (mean over all pixels and all RGB channels). If the mean intensity is strictly less than 5.0, classify the frame as `"black"`.
   - **Distance Metric**: The Mean Absolute Error (MAE) in pixel intensity between the current frame and the *immediately preceding* frame. If the frame is not black, and the MAE is strictly less than 1.0, classify it as `"duplicate"`. 
   - Note: The very first frame (frame_0001.jpg) cannot be a duplicate. If a frame is neither "black" nor "duplicate", it is `"clean"`.

3. **Metadata Generation**:
   The Python pipeline must output a JSON file at `/home/user/manifest.json` with the following structure:
   ```json
   {
     "summary": {
       "total_frames": X,
       "black_frames": Y,
       "duplicate_frames": Z,
       "clean_frames": W
     },
     "frames": {
       "frame_0001.jpg": "clean",
       "frame_0002.jpg": "duplicate",
       ...
     }
   }
   ```

4. **Serve the Results (Multi-protocol)**:
   Write and start a Python HTTP server (e.g., using `http.server`, `Flask`, or `FastAPI`) listening precisely on `127.0.0.1:9090`.
   The server must require an HTTP header `Authorization: Bearer SECRET_DATA_TOKEN` for all requests. If the header is missing or incorrect, return a 401 Unauthorized status.
   
   The server must expose these endpoints:
   - `GET /summary`: Returns the `summary` object from your manifest as JSON.
   - `GET /frame/<filename>`: (e.g., `/frame/frame_0050.jpg`) Returns a JSON object `{"status": "<classification>"}` where classification is `"black"`, `"duplicate"`, or `"clean"`. If the frame doesn't exist, return a 404.

Once you have generated the manifest and started the server in the background, you have completed the task.