We are migrating a legacy Python-based drone telemetry processing system to a minimal edge-container environment. The old Python package `aero-math-router` has a broken `setup.py` and relies on outdated, bloated dependencies. We need you to port its core routing and validation logic to pure Bash.

Your task is to write a standalone Bash script at `/home/user/validate_telemetry.sh` that acts as a secure URL router and mathematical parameter validator for incoming telemetry requests.

**Context & Requirements:**
1. **The Calibration Video:** The validation logic requires a specific "base modulo" dynamically calculated from a calibration video located at `/app/calibration.mp4`. You must extract the video and determine the exact total number of frames in this video. Let this integer be `N`. The base modulo for all mathematical validation is `M = N % 100`. (You may use `ffmpeg` or `ffprobe`, which are pre-installed).
2. **The Telemetry Router:** Your Bash script must accept a single argument: a URL path representing a telemetry API call.
   Expected format: `/api/v1/route/<action>?<params>`
   Example: `/api/v1/route/calculate?x=15&y=20`
3. **Validation Rules (The Filter):**
   Your script must exit with code `0` (clean/accept) ONLY if ALL the following conditions are met. Otherwise, it must exit with code `1` (evil/reject).
   - The URL path must exactly match `/api/v1/route/calculate` or `/api/v1/route/update`.
   - The parameters must only contain keys `x` and `y`.
   - The values of `x` and `y` must be strict positive integers (no decimals, no negative numbers, no bash command injections, no special characters).
   - **Mathematical Constraint:** The sum of `x` and `y` must be perfectly divisible by the base modulo `M` calculated from the video.
   - Any URL encoding, path traversal attempts (`../`), or malformed query strings should be rejected.

Write your implementation in `/home/user/validate_telemetry.sh` and make sure it is executable. Your script will be evaluated against a large suite of valid and malicious requests.