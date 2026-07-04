You are a container specialist managing a new microservices environment. We need to deploy a local video-processing microservice and configure the environment according to our standards. 

Complete the following tasks:

1. **Storage/Fstab Text Processing Pipeline**
   You have been provided a mock fstab file at `/app/fstab.mock` representing the intended host storage. 
   Write a script or command pipeline that parses `/app/fstab.mock` and extracts the mount point paths (the second column) for all entries that use either the `ext4` or `xfs` filesystem. Save these absolute paths (one per line) to `/home/user/active_mounts.txt`.

2. **Video Frame Extraction**
   Our ingestion system placed a test video at `/app/test_video.mp4`. 
   Create a directory `/home/user/data/frames/`. Use `ffmpeg` to extract frames from the video at exactly 2 frames per second (fps). Save the extracted frames as JPEG images in this directory using the format `frame_0001.jpg`, `frame_0002.jpg`, etc.

3. **Rust Microservice**
   Create a Rust application in `/home/user/frame_service` (using `cargo new`). Write a custom HTTP server using Rust's standard library `std::net::TcpListener` (or a lightweight crate if you prefer, but standard library is faster to compile).
   The service must:
   - Listen continuously on `127.0.0.1:9090`.
   - Implement an HTTP `GET /metrics` endpoint.
   - Require authentication: it must check for the HTTP header `X-Service-Auth: v1-alpha-xyz`. If missing or incorrect, return a `401 Unauthorized` HTTP response.
   - If authenticated, it must dynamically count the number of files currently present in `/home/user/data/frames/`.
   - Return a `200 OK` HTTP response with a JSON body exactly like this: `{"fps": 2, "extracted_frames": <N>}` (where `<N>` is the counted number of files).
   - Append a line to `/home/user/logs/microservice.log` for every incoming request (regardless of auth success) in the format: `[<DATE_TIME>] <METHOD> <PATH> <STATUS_CODE>`.

4. **Log Rotation Configuration**
   Create a logrotate configuration file at `/home/user/logrotate.conf` specifically for `/home/user/logs/microservice.log`. 
   Configure it so that the log is rotated when it reaches `1M` in size, keep `3` old copies, compress the rotated files, and create a new log file with `0644 user user` permissions.

5. **Service Startup Automation**
   Write a bash script at `/home/user/run.sh` that:
   - Ensures the `/home/user/logs/` directory exists.
   - Compiles and runs the Rust microservice in the background.
   - Detaches the process so it remains running.

Run your `/home/user/run.sh` script to bring the service online before finishing the task.