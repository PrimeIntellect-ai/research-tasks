You are acting as a Site Reliability Engineer responding to an incident. Our primary video analytics service, written in Rust, has gone offline. The service processes incident videos, logs metadata to a SQLite database, and exposes an HTTP API for metrics and a gRPC API for queries. 

Unfortunately, the last deployment broke the build, the frame processing logic hangs indefinitely, and the local SQLite database got corrupted during the crash.

Your objectives:
1. **Build Failure Diagnosis:** The Rust project is located at `/home/user/video_service`. It currently fails to compile. Identify and fix the build errors (there is a missing dependency in `Cargo.toml` and a syntax error in `src/main.rs`).
2. **Database Recovery:** There is a corrupted SQLite database at `/home/user/video_service/data/metrics.db`. Recover the data from it and save the clean database to `/home/user/video_service/data/recovered.db`. The table `video_stats` should be intact.
3. **Loop/Boundary Fix:** The frame processing module (`src/processor.rs`) attempts to count the frames of the video located at `/app/incident.mp4` using `ffprobe` or `ffmpeg`, but an off-by-one error and a bad loop condition cause it to hang or panic. Fix the logic so it correctly calculates and returns the exact number of frames in the video.
4. **Service Restoration:** Once fixed, run the service. The service must start and bind to the following ports:
   - **HTTP Server:** Listen on `127.0.0.1:8080`. 
     - `GET /health` must return HTTP 200 with JSON `{"status": "ok"}`.
     - `GET /metrics` must require a Bearer token matching the `SERVICE_TOKEN` environment variable (which you must set to `secret-uptime-token-99` when running the service). If correct, it returns HTTP 200.
   - **gRPC Server:** Listen on `127.0.0.1:50051`. It serves the `video.VideoService` with a single method `GetFrameCount`. This method takes an empty request and must return a response containing the exact frame count of `/app/incident.mp4` as processed by your fixed logic.

Ensure the service remains running in the background so our automated verifiers can connect to it using both HTTP and gRPC. Do not change the service definitions or protobuf files.