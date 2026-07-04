As a security engineer, you need to rotate the credentials and update the Intrusion Detection System (IDS) filters for our proprietary backend service. The new configuration has been securely transmitted to you via a video file to prevent automated scraping by basic malware. 

Your task involves extracting the new configuration from the video, and implementing a C++ filter that rigidly applies these new rules.

**Step 1: Extract the Configuration**
You have been provided with a video file at `/app/rotation_data.mp4`. The video encodes the new configuration as a sequence of flashing colors, with one frame representing one bit:
- A predominantly **Red** frame (mean Red channel > 128, Green/Blue < 50) represents a `1`.
- A predominantly **Green** frame (mean Green channel > 128, Red/Blue < 50) represents a `0`.
- The sequence of bits forms an 8-bit ASCII string.
- The decoded string is in the format: `CREDENTIAL|<secret_token>|CSP|<csp_value>|BLOCK|<malicious_word>`

**Step 2: Implement the Filter**
Write a C++ program at `/home/user/filter.cpp` and compile it to `/home/user/filter`. This program will act as a strict pre-processor. It must read the entire input from standard input (`stdin`).

The input format is defined as:
Line 1: `AUTH <token>` (ended by `\n`)
Line 2: An empty line (`\n`)
Remaining input: The request body.

Your program must enforce the following rules in order:
1. **Authentication**: If Line 1 does not exactly match `AUTH <secret_token>` (where `<secret_token>` is the one extracted from the video), print exactly `401\n` to `stdout` and exit with code `1`.
2. **IDS Pattern Matching**: If the remaining request body contains the exact string `<malicious_word>` anywhere, print exactly `403\n` to `stdout` and exit with code `1`.
3. **Success & CSP Enforcement**: If both checks pass, print exactly `200\nCSP: <csp_value>\n` followed immediately by the exact request body to `stdout`, and exit with code `0`.

If the input does not even contain two newline characters to separate the headers from the body, treat it as a malformed body and only perform the Authentication check. If auth passes but the format is malformed (no empty line), print `400\n` and exit with code `1`.

We will run a rigorous equivalence fuzzing test against your `/home/user/filter` executable to ensure it behaves exactly identically to our reference implementation under all possible inputs.