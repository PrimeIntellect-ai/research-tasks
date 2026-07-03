You are a systems programmer working on a video analysis pipeline. We have a Python application that uses a C library for fast numerical computations, but the library is currently failing to link properly, and the application needs to be finished and exposed via a REST API.

Your objective is to fix the linking issue, implement the video processing pipeline, perform a database schema migration, and expose the results via a web service.

Here are the specific requirements:

1. **Fix the C Library Linking Issue**
   In `/home/user/mathlib/`, there is a C library intended to calculate the maximum rolling standard deviation of an array of floats.
   - Currently, running `make` builds `libmathops.so`, but loading it in Python fails with an undefined symbol error related to math functions.
   - Fix the `Makefile` so it correctly links the standard math library, and recompile `libmathops.so`.

2. **Video Processing & Custom Data Structure**
   - You must process the video located at `/app/video.mp4`.
   - Using Python (you may install `opencv-python` or use `ffmpeg`), read the video frame by frame.
   - For each frame, calculate the average pixel brightness (convert the frame to grayscale, sum all pixel values, and divide by the total number of pixels).
   - Store these average brightness values in an ordered array/list.
   - Use `ctypes` to pass this array of `double`s to the C function `double compute_max_variation(double* values, int length, int window_size);` in `libmathops.so`.
   - Set `window_size = 5`. The function returns the maximum standard deviation found across any sliding window of 5 frames.

3. **Schema Migration**
   - There is a SQLite database at `/home/user/db/metrics.db` with a table `video_stats` (schema: `id INTEGER PRIMARY KEY, filename TEXT`).
   - Write a Python script or SQL command to migrate this schema by adding a new column: `max_variation REAL`.

4. **REST API Service**
   - Create a FastAPI application listening on `127.0.0.1:8000`.
   - Implement an endpoint `GET /api/v1/process`.
   - When requested, this endpoint must:
     a. Process `/app/video.mp4` as described above.
     b. Insert a new row into the `video_stats` table with `filename = 'video.mp4'` and the calculated `max_variation`.
     c. Return a JSON response: `{"status": "ok", "max_variation": <calculated_value>}`.

Ensure your FastAPI server is running in the background when you consider the task complete so that the automated verifier can test the endpoint. You may use a virtual environment in `/home/user/venv`.