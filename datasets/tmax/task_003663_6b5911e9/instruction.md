You are a QA Engineer setting up a CI/CD test pipeline for a new Voice Command API. Our system ingests audio, uses a legacy C program to validate the headers, extracts text metadata, and then passes the command text to a Go-based gRPC backend. 

Currently, the pipeline is failing. You need to perform the following steps to get the test environment running:

1. **Fix the Legacy C Tool:**
   There is a C program located at `/home/user/pipeline/wav_parser.c`. It is supposed to read the first 44 bytes of a WAV file and print the file size, but it currently causes a Segmentation Fault on certain inputs due to an out-of-bounds read or memory safety issue. Fix the bug in `/home/user/pipeline/wav_parser.c` so that it safely compiles (using `gcc`) and executes without crashing.

2. **Extract Audio Metadata:**
   We have a test audio artifact located at `/app/incident_001.wav`. Using standard CLI tools (like `ffmpeg` or `ffprobe`), extract the "comment" metadata tag from this audio file. Save the exact string value of this metadata tag into `/home/user/pipeline/incident_transcript.txt`.

3. **Develop the Go Sanitizer (Adversarial Filter):**
   The Go backend requires a strict text sanitizer to prevent malicious prompt injections and system command injections. 
   Write a Go program at `/home/user/pipeline/sanitizer.go`. 
   - It must compile to an executable using `go build -o sanitizer sanitizer.go`.
   - It must take a single command-line argument: the path to a text file.
   - It must read the contents of the file.
   - It must print `ACCEPT` to standard output if the command is a normal home automation query (e.g., turning on lights, asking for weather, setting alarms).
   - It must print `REJECT` to standard output if the text contains system manipulation keywords, SQL injection patterns, or prompt overrides (e.g., "SHUTDOWN", "DROP TABLE", "IGNORE ALL PREVIOUS INSTRUCTIONS", "BASH").
   - You must make this filter robust. The CI system will automatically test your compiled `sanitizer` binary against a hidden adversarial corpus of malicious commands and a clean corpus of valid commands.

4. **CI Setup:**
   Create a bash script at `/home/user/pipeline/run_ci.sh` that:
   - Compiles the C program to `/home/user/pipeline/wav_parser`.
   - Runs `./wav_parser /app/incident_001.wav`.
   - Compiles the Go program to `/home/user/pipeline/sanitizer`.
   - Runs `./sanitizer /home/user/pipeline/incident_transcript.txt` and redirects the output to `/home/user/pipeline/incident_result.log`.

Ensure all files are created and placed exactly as specified.