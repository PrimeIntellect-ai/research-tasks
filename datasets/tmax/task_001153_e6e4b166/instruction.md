You are an application performance engineer debugging a custom C-based streaming HTTP server located in a Git repository at `/home/user/audiostreamer`. The system has recently suffered from a severe regression and currently fails to even compile. Once compiled, it reportedly suffers from a 100% CPU lockup when handling certain requests due to a subtle timezone-related logic bug.

Your objectives are to fix the build, resolve the performance issue, recover a lost configuration, extract critical setup information from an audio incident report, and deploy the fixed server.

Follow these steps exactly:

1. **Build Failure Diagnosis:**
   Inspect the C source code in `/home/user/audiostreamer`. Find and fix the compilation errors. The application uses a standard `Makefile`. You must be able to run `make` successfully.

2. **Codebase Comprehension & Performance Debugging:**
   The server has a custom request-logging function that parses timestamps. However, an engineer recently introduced a subtle timezone bug involving `mktime` and `gmtime` that causes an infinite loop under certain conditions. Identify the bottleneck, isolate the buggy function (you may want to write a minimal reproducible example to test it locally), and fix the C code so it performs correctly without locking up the CPU.

3. **Git Forensics:**
   The server requires an authentication token to be passed via the `AUTH_TOKEN` environment variable, but the documentation was lost. The token was hardcoded in an old configuration file that was subsequently deleted from the Git repository. Dig through the Git history to recover this 16-character alphanumeric token.

4. **Audio Artefact Transcription:**
   There is an emergency incident report recorded in an audio file located at `/app/incident_report.wav`. You must process or transcribe this audio file (a local installation of `whisper-cli` or similar tools may be used, or you can download it to listen if your environment permits). The spoken audio contains the exact timezone string (e.g., "America/New_York") that the server expects in the `SERVER_TZ` environment variable.

5. **Deployment:**
   Set the required environment variables (`AUTH_TOKEN` and `SERVER_TZ`). Run the fixed server so that it binds to `0.0.0.0:8080`. The server exposes a simple HTTP API. Leave the server running in the background.

The automated verification system will send real HTTP GET requests to your server at `127.0.0.1:8080` to verify its availability, the correctness of the timezone parsing fix, and the validity of the authentication token.