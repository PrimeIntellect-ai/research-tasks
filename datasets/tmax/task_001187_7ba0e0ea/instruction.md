You are an observability engineer tasked with updating our dashboard normalization pipeline after a recent post-mortem. The post-mortem meeting was recorded, and the specific new normalization rules were dictated in an audio log. 

Your task consists of three parts: extracting the logic, implementing a high-performance C++ parser, and creating an idempotent deployment script.

Part 1: Logic Extraction
There is an audio file at `/app/incident_094.wav`. Use any available transcription tool (e.g., `whisper` or `ffmpeg`-based pipelines installed in the system) to recover the spoken content. The audio contains the exact mathematical rules and output formats required for the new dashboard parser.

Part 2: C++ Implementation
Write a C++ program at `/home/user/parser.cpp` that reads a stream of metric events from standard input. 
- The input consists of space-separated pairs of `SUBSYSTEM` (string) and `VALUE` (integer). Example: `CPU 40 DISK 100 NETWORK 55 MEM 1024`.
- The program must apply the normalization rules extracted from the audio recording.
- The program must output the final formatted metrics to standard output.
- Compile your program to `/home/user/dashboard_parser`. 

Part 3: Staged Idempotent Deployment & Permissions
We use a custom, bash-only deployment system. Write a shell script at `/home/user/deploy.sh` that performs the following actions idempotently (running it multiple times must result in the exact same system state without errors):
1. Creates the directories `/home/user/deploy/staging/bin` and `/home/user/deploy/production/bin`.
2. Sets the permissions of the `deploy`, `staging`, and `production` directories (and their `bin` subdirectories) to exactly `0755`.
3. Copies `/home/user/dashboard_parser` into both `staging/bin/` and `production/bin/`.
4. Sets the permissions of the copied `dashboard_parser` binaries to strictly read-only and executable (`0555`).

Once you have written and compiled the C++ program, run your `/home/user/deploy.sh` script to finalize the deployment. The automated verifier will aggressively fuzz your deployed `/home/user/deploy/production/bin/dashboard_parser` binary against an internal oracle with thousands of random inputs to ensure bit-exact output matching.