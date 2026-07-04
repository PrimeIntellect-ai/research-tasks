You are a data analyst working with surveillance footage. We need you to build a Go-based ETL pipeline, feature extraction, and search service. 

We have a 10-second video located at `/app/data/surveillance.mp4` and a CSV file with metadata at `/app/data/events.csv`. The CSV has the columns: `timestamp_sec`, `event_name`, and `camera_id`.

Your task involves building an end-to-end Go application that does the following:

1. **Video Extraction**: Extract 1 frame per second from `/app/data/surveillance.mp4` starting at second 0 (so you should get frames for 0s, 1s, ..., up to the end of the video). Save them in `/app/processed/frames/` as `frame_0.jpg`, `frame_1.jpg`, etc. You can use the pre-installed `ffmpeg` via your Go code or bash script.

2. **Embedding Computation**: Write a Go function that takes a frame image, converts it to grayscale, and computes a "pseudo-embedding" of 16 float64 values. The embedding is created by dividing the image into a 4x4 grid (16 cells total, going left-to-right, top-to-bottom). For each cell, calculate the average grayscale pixel value (from 0 to 255) and normalize it to a 0.0 - 1.0 range (divide by 255.0). 

3. **Data Joining & Storage**: Join these embeddings with the data from `/app/data/events.csv` by matching the frame's second (`0` to `9`) with the `timestamp_sec` in the CSV. Store the resulting records (timestamp, event_name, camera_id, and the 16-dimensional float vector) in an SQLite database at `/app/processed/vector_store.db`.

4. **Inference Benchmarking**: Write a standard Go benchmark (`BenchmarkEmbedding` in a `_test.go` file) that measures the performance of your pseudo-embedding function on a single frame. Run this benchmark and redirect the output to `/app/processed/benchmark.txt`.

5. **API Service**: Write and start an HTTP server in Go that listens on `0.0.0.0:8080`.
   - Endpoint: `GET /search`
   - Query Parameter: `vector` - a comma-separated list of 16 floats.
   - Header: Must require authentication via the header `Authorization: Bearer ds-api-token`. If missing or incorrect, return HTTP 401.
   - Behavior: Compute the cosine similarity between the queried vector and all stored embeddings in the database. 
   - Response: Return an `application/json` payload representing the most similar record:
     `{"timestamp": <int>, "event_name": "<string>", "camera_id": "<string>"}`

Ensure the HTTP server remains running in the background or foreground so it can be tested. All Go source code should be placed in `/app/src/`. Ensure the directories exist before running your application.