You are an operations engineer triaging an incident. Our mathematical frame-analysis pipeline, entirely written in Bash, has started failing on our new edge servers. The pipeline processes surveillance video and extracts pixel-intensity differentials across frames. However, recent changes introduced a regression: intermediate mathematical state tracing occasionally produces negative values for what should be strictly monotonically increasing frame-intensity accumulators. We suspect a signed integer overflow in the Bash 64-bit arithmetic evaluation `$(())` logic, introduced recently in our Git repository.

Your task involves three parts:

1. **Git Bisection:** 
A Git repository exists at `/home/user/pipeline`. The `main` branch HEAD is failing, but the tag `v1.0-stable` is known to be good. Use `git bisect` to identify the exact commit that introduced the overflow bug. Write the full 40-character SHA-1 hash of the bad commit to `/home/user/bad_commit.log`.

2. **Video Fixture Analysis & Patching:**
We have a test video fixture located at `/app/incident_capture.mp4`. The pipeline script (`/home/user/pipeline/process_video.sh`) is supposed to extract frames using `ffmpeg`, calculate cumulative intensity diffs, and output a bounding box detection trace. Fix the bug in `process_video.sh` so it uses `bc` or `awk` to handle arbitrarily large integers, preventing the overflow. Run the fixed script against `/app/incident_capture.mp4` and save the standard output (which prints frame numbers and detection flags) to `/home/user/video_analysis.log`.

3. **Adversarial Sanitizer:**
Before the fix is fully deployed, we need a robust input sanitization layer. Create a Bash script at `/home/user/sanitizer.sh`. It must accept a file path as an argument (e.g., `./sanitizer.sh /path/to/frame_trace.txt`). The script must exit with code 0 if the trace file contains valid, non-overflowing monotonically increasing mathematical accumulations (clean), and exit with code 1 if it detects simulated overflow artifacts (evil/anomalous). We will test this against two hidden corpora of trace files.

Ensure your sanitizer works flawlessly. The system relies on accurate trace sanitization to prevent downstream database corruption.