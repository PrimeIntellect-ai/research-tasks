You are an incident responder investigating a recent system breach where an attacker was able to forge administrative authentication tokens. We have secured two key pieces of evidence from the compromised authentication server:

1. A stripped Linux executable located at `/app/auth_oracle`. This binary was left behind by the attacker and appears to be the tool they used to generate forged tokens. It accepts three arguments: a 32-bit integer salt (in decimal format), a `user_id` string, and a Unix `timestamp`.
2. A screen recording of the attacker's terminal during the breach, located at `/app/breach_recording.mp4`. The attacker obfuscated the exact secret salt they used, but our forensics team noted that the video contains a sequence of solid colored frames injected by the attacker's custom terminal setup.

Your task is to fully reconstruct the token generation logic into a standalone Python script.

Phase 1: Video Analysis
Extract the hidden 32-bit salt from `/app/breach_recording.mp4`. The video is exactly 32 seconds long and runs at 1 frame per second (32 frames total). Each frame is completely filled with a solid color: either pure Red (#FF0000) or pure Blue (#0000FF). 
- A Red frame represents the binary digit `0`.
- A Blue frame represents the binary digit `1`.
Read the frames in chronological order (from frame 1 to 32) to form a 32-bit binary number (Most Significant Bit first). Convert this binary string into its decimal integer representation. This is the secret salt.

Phase 2: Reverse Engineering
Analyze the provided `/app/auth_oracle` binary to understand the exact cryptographic transformations it applies to the salt, `user_id`, and `timestamp` to produce the final authentication token. You will need to disassemble or decompile the binary to understand the custom hashing and formatting mechanism.

Phase 3: Reimplementation
Write a Python script at `/home/user/token_gen.py` that perfectly replicates the token generation algorithm used by the attacker for *any* given user ID and timestamp, using the secret salt recovered from the video.

Your script must accept exactly two positional command-line arguments:
`python3 /home/user/token_gen.py <user_id> <timestamp>`

The script must print only the final generated token to standard output (no extra spaces, no debug text). The automated verification system will extensively test your Python script against the compiled oracle using thousands of random inputs. Your script's output must be bit-for-bit identical to what `/app/auth_oracle <secret_salt> <user_id> <timestamp>` would produce.