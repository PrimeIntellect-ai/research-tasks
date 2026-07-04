As a release manager preparing our upcoming deployments, I need you to implement a build log parser. 

We had a small C project that frequently suffered from linking errors and deployment failures due to out-of-order build steps and too many validation retries. To enforce our new build policy, I created a short screen recording demonstrating the correct deployment state machine and the rate-limiting rules. The video is located at `/app/release_demo.mp4`.

Please write a Python script at `/home/user/release_parser.py` that acts as a strict state machine parser for our deployment logs. 

Your script must:
1. Read a sequence of log events from standard input (`stdin`), one per line.
2. Track the deployment state and validation retries based on the rules shown in `/app/release_demo.mp4`. 
3. If the script reads `VALIDATION_FAILED`, it should increment the retry counter. If this counter strictly exceeds the maximum allowed retries (the rate limit specified in the video), immediately print `RATE_LIMIT_EXCEEDED` and exit with code 1.
4. If the script reads `STATE: <NAME>` (e.g., `STATE: BUILD`), it must transition to that state. The system starts implicitly in the state *before* the first one shown in the video sequence (i.e., it expects the first state transition to be the first state in the video).
5. If a state transition occurs out of the exact sequential order defined in the video, immediately print `LINKING_ERROR` and exit with code 1.
6. If the state machine successfully reaches the final state in the sequence without exceeding the validation rate limit or violating the state order, immediately print `SUCCESS` and exit with code 0.
7. Ignore any lines that do not match `VALIDATION_FAILED` or `STATE: <NAME>`.

You can use standard tools like `ffmpeg` to extract and examine the frames of the video to discover the required state sequence and the exact rate limit.

Your script will be tested against a massive suite of randomly generated build logs to ensure it strictly conforms to the expected behavior. Ensure it is robust and handles standard input efficiently.