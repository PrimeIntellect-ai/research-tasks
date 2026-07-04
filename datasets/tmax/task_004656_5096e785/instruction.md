You are a security engineer tasked with rotating credentials and sanitizing leaked data. An automated security scanner detected that a set of spoken credentials was inadvertently recorded into a system audio token used for physical access. 

The audio file is located at `/app/token.wav` (Format: 44.1kHz, 16-bit PCM, Mono).
The security log detailing the exact moments of the leakage is located at `/home/user/audit.log`.

Your task is to write a Rust program that performs the following steps:
1. Parse `/home/user/audit.log` to identify the start times and durations of the credential leaks.
2. Read `/app/token.wav`.
3. Enforce our data sanitization policy by completely zeroing out (setting the amplitude to exactly 0) the audio samples during the leaked intervals. Use standard sample rate math (e.g., sample_index = time_in_seconds * 44100).
4. Save the sanitized audio to `/home/user/redacted.wav`.
5. Ensure strict access control by setting the permissions of `/home/user/redacted.wav` to exactly `600` (read and write for the owner only).

The `audit.log` contains entries in the following format:
`[CRITICAL] Leakage detected - start: 2.500s, duration: 1.200s`

You may use standard Rust crates (like `hound` for WAV processing) by creating a new Cargo project in `/home/user/redact_tool`. Once your Rust program finishes processing, the automated test will verify the metric accuracy of your redacted WAV file against a known ground truth.