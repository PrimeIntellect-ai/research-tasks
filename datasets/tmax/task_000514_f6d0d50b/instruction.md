You are an infrastructure script developer for a cloud video processing service. Your task is to build a robust job validation pipeline and extract video metadata, combining request validation, C program debugging, and Bash scripting.

There are three parts to this task:

**Part 1: Repair the Rate Limiter (C & Makefile)**
In `/home/user/rate_limiter/`, there is a small C utility `rl_check.c` and a `Makefile`. This utility takes a user token as a command-line argument and validates its format to prevent abuse. 
1. The `Makefile` is broken and fails to build.
2. The `rl_check.c` program has bugs (including a potential segmentation fault and missing standard includes) that prevent it from compiling and running reliably.
Repair both files so that running `make` successfully produces the executable `/home/user/rate_limiter/rl_check`. The compiled program should exit with status `0` if the token is exactly 10 alphanumeric characters, and `1` otherwise.

**Part 2: Build the Job Validator (Bash)**
You must create a Bash script at `/home/user/validate_job.sh`. This script acts as a security filter for incoming JSON job requests to our `ffmpeg` rendering queue.
* Usage: `/home/user/validate_job.sh <path_to_json_file>`
* The script must parse the JSON (using `jq`) which contains the fields: `video`, `timestamp`, `filters`, and `token`.
* **Validation Rules:**
  - `video`: Must be a strict filename ending in `.mp4` containing only alphanumeric characters and underscores (e.g., `vid_1.mp4`). No slashes or path traversal `..` allowed.
  - `timestamp`: Must exactly match the format `HH:MM:SS` (e.g., `00:00:15`).
  - `filters`: Must contain strictly alphanumeric characters, commas, and equals signs (e.g., `scale=320,vflip`). No shell metacharacters like `;`, `$`, `|`, etc.
  - `token`: Must be validated by passing it to your compiled `/home/user/rate_limiter/rl_check` utility.
* If *all* validations pass and the rate limiter exits `0`, your script must exit with status `0`.
* If *any* validation fails, or if the JSON is malformed, your script must exit with a non-zero status (e.g., `1`).

**Part 3: Benchmark and Execution (Video Fixture)**
A master job file is provided at `/app/master_job.json`, alongside a dashcam recording at `/app/dashcam.mp4`.
1. Run your `validate_job.sh` against `/app/master_job.json`. (It is a valid job and should pass).
2. Using `ffmpeg`, manually extract the exact single frame from `/app/dashcam.mp4` at the `timestamp` specified in `/app/master_job.json`, applying the `filters` specified in the JSON. Save the extracted frame to `/home/user/output_frame.jpg`.
3. Wrap your `ffmpeg` extraction command in a simple bash benchmarking script using the `/usr/bin/time -v` command. Redirect the verbose timing output to `/home/user/benchmark.txt`.

Ensure all file paths and names match the requirements exactly. Your `validate_job.sh` will be heavily tested against hidden corpora of malicious and clean payloads.