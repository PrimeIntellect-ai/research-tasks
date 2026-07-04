You are tasked with building a streaming configuration log processor. We have a configuration manager that tracks changes, but the logs are sometimes corrupted, values are missing, and payloads are encoded in different formats. 

Your goal is to write a Python script at `/home/user/parse_log.py` that reads these log lines from `stdin` and writes processed output to `stdout`.

Because our team leader left a voice memo detailing the exact business rules for time-based bucketing and imputation, you must first transcribe the audio file located at `/app/rules.wav`. Use an appropriate command-line transcription tool (like Whisper, which you may need to install or use an available API) to recover the spoken rules.

The input lines on `stdin` will follow this exact format:
`[TIMESTAMP] {ENCODING} - PAYLOAD`

Where:
- `TIMESTAMP` is a Unix epoch integer.
- `ENCODING` is either `b64` (Base64) or `hex` (Hexadecimal).
- `PAYLOAD` is the encoded string.

When decoded using the specified encoding (and decoded as UTF-8), the payload will be in the format `KEY=VALUE`. 
Sometimes the `VALUE` is empty (e.g., `KEY=`).

Your script `/home/user/parse_log.py` must:
1. Use Regex to extract the timestamp, encoding, and payload. Ignore any lines that do not strictly match the format.
2. Decode the payload. If decoding fails or the result doesn't contain a `=`, ignore the line.
3. Group the events into time buckets. The bucket size is specified in the audio recording `/app/rules.wav`. The bucket identifier should be the floored start time of the bucket (e.g., `(timestamp // bucket_size) * bucket_size`).
4. If a `VALUE` is empty, you must impute it according to the fallback rule described in `/app/rules.wav`.
5. For each valid line, output a single line to `stdout` in the format: `bucket,key,value`.

Your script must be robust, memory-efficient (streaming large files), and produce exactly the expected output for any valid input sequence. Automated tests will verify your program's exact output against a hidden oracle using random inputs.