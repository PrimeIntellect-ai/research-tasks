Wake up, you're on call! It's 3:00 AM and our security monitoring pipeline just went down after a botched deployment. We need you to restore the service immediately.

There are two major issues:
1. The CCTV flash detection service is failing to build and run.
2. The log ingestion endpoint is being bombarded with malformed payloads that crash our downstream serializers.

**Part 1: Fix the Flash Detector**
The codebase is located at `/app/service/`. 
- The `requirements.txt` has a dependency conflict preventing installation. Fix the dependencies so the environment can be built successfully.
- The script `flash_detector.py` processes the video `/app/cctv_feed.mp4` to count the number of times a bright flash occurs. It calculates frame luminance, but the developer botched the formula and color space conversion (OpenCV loads in BGR, but the formula expects RGB, and the weighting is wrong). Fix the implementation so that running `python flash_detector.py /app/cctv_feed.mp4` outputs the correct number of flashes to a file `/home/user/flash_count.txt`. 

**Part 2: Log Sanitizer (Adversarial Corpus)**
Our pipeline ingests JSON logs, but attackers are sending corrupted files containing invalid byte sequences, mixed encodings, and malicious serialization structures that cause our Python backend to throw exceptions.
You must write a log sanitizer script at `/home/user/sanitizer.py`.
- It must take a single file path as an argument: `python /home/user/sanitizer.py <path_to_log>`
- If the log is valid, properly UTF-8 encoded JSON matching our schema (requires a "timestamp" string and a "sensor_data" dictionary), it must exit with code 0.
- If the log contains encoding errors (e.g., invalid UTF-8 bytes), serialization corruption, or missing required schema fields, it must reject it by exiting with code 1.

We will verify your `sanitizer.py` against our internal corpora of clean and evil logs. It must preserve 100% of the clean logs (exit 0) and reject 100% of the evil logs (exit 1).

Please fix the service and create the sanitizer script.