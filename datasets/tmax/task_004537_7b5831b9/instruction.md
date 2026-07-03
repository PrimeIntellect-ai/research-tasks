You are an operations engineer triaging an incident. A downstream computer vision pipeline is crashing due to a "convergence failure" caused by a specific corrupted frame in a recent video capture.

We have isolated the video to `/app/incident_capture.mp4`.

An intern wrote a Bash script at `/app/bisect_anomaly.sh` that uses `ffmpeg` and delta debugging (bisection) to find the corrupted frame. A corrupted frame in this video is characterized by being completely black (average brightness / Y-channel value drops close to 0), whereas normal frames are white/gray. 

However, the script has a bug: it fails to converge and loops infinitely or errors out (convergence failure). 

Your task:
1. Use interactive debugging (e.g., `bash -x`) to identify why `/app/bisect_anomaly.sh` is failing to converge.
2. Fix the Bash script so that it correctly identifies the corrupted frame number.
3. Run the fixed script to find the exact corrupted frame number in `/app/incident_capture.mp4`.
4. Stand up a simple HTTP service listening on `127.0.0.1:8888`. 
5. When this service receives a `GET /anomaly` request, it must return an `HTTP 200 OK` response with a JSON body containing the anomalous frame number. The JSON format must be exactly: `{"frame": <FRAME_NUMBER>}`.

You may use standard CLI tools (like `nc`, `python3`, `bash`, `awk`, `ffmpeg`) to accomplish this. The service must run in the background and remain active for verification.