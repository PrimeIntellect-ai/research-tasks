You are an infrastructure engineer automating the deployment of a new telemetry video analysis pipeline. The goal is to set up a version-controlled deployment pipeline, configure local log management, set up a network proxy, and implement a highly optimized Python video analyzer.

Complete the following tasks entirely within the `/home/user` directory without using root or `sudo`:

1. **Local Network Proxy:**
   We need to route traffic from a legacy ingestion port to our new telemetry service port. Use `socat` to forward TCP connections from local port 8080 to local port 5000. Run this process in the background and write its exact Process ID (PID) to `/home/user/proxy.pid`.

2. **Log Management Setup:**
   The new service will write logs to `/home/user/logs/telemetry.log`. Create the directory and write a `logrotate` configuration file at `/home/user/logrotate.conf` that specifically manages this log file with the following rules:
   - Rotate daily
   - Keep exactly 5 rotated backlogs
   - Compress the rotated logs
   - Do not error out if the log file is missing

3. **Deployment Pipeline (Git Server & Hooks):**
   - Initialize a bare Git repository at `/home/user/telemetry.git`.
   - Clone it to `/home/user/workspace`.
   - Create a `post-receive` hook in the bare repository. When code is pushed to the `master` branch, the hook must:
     a) Check out the latest code to `/home/user/deploy/`. (You must create this deployment directory).
     b) Execute the Python script `analyze.py` (which will be deployed there) with the argument `/app/telemetry.mp4`.
     c) Append the output of the script to `/home/user/logs/telemetry.log`.
   Ensure the hook is executable.

4. **Optimized Video Telemetry Processor:**
   In your cloned `/home/user/workspace` directory, write a Python script named `analyze.py`. 
   - The script must take one argument: the path to a video file.
   - It will analyze `/app/telemetry.mp4`, which contains 30 seconds of telemetry data at 30 fps.
   - **The Task:** Find every frame where the top-left 50x50 pixel region is predominantly pure red (average value of the Red channel > 150, while Green and Blue are < 50).
   - **The Output:** The script must print a single integer to standard output representing the total count of "red" frames detected.
   - **The Performance Constraint:** Your code must be heavily optimized using OpenCV (`cv2`) and vectorized `numpy` operations. Naive frame-by-frame Python loops will be too slow. The automated verifier will measure the execution time of your script. It must process the entire video and exit in under 1.5 seconds.
   
   Once `analyze.py` is written, commit and push it to the bare repository to trigger your pipeline and generate the initial log entry.