You are an engineer tasked with setting up a custom, voice-activated CI/CD build agent from scratch. The agent must handle data processing, dependency validation, semantic version checks, and memory profiling. 

You must write a Python HTTP server that listens on `127.0.0.1:8080`. You may use standard libraries, `FastAPI`, `Flask`, or `http.server`. You will also need to install an audio transcription library like `openai-whisper` (or use `speechrecognition` with a local backend) to process audio files.

Here are the requirements for your build system:

1. **Environment Setup:**
   Create a virtual environment at `/home/user/venv` and install all necessary dependencies for your server and audio transcription.

2. **The Build Agent Service:**
   Your server must run continuously on `127.0.0.1:8080` and expose two REST endpoints:
   
   - `GET /health`: Must return an HTTP 200 with the JSON response `{"status": "ok"}`.
   
   - `POST /build`: When hit, the server must perform a multi-stage pipeline:
     
     **Stage A: Audio Transcription & Semantic Versioning**
     - Read the audio fixture located at `/app/build_command.wav`.
     - Transcribe the audio to text. The audio contains a phrase like "Initiate build for version X point Y point Z".
     - Extract the semantic version (e.g., "two point one point zero" becomes "2.1.0").
     - Read the current deployed version from `/app/current_version.txt`.
     - Compare the two semantic versions. If the spoken version is not strictly greater than the current version, return an HTTP 400 with `{"error": "version downgrade"}`.
     
     **Stage B: Dependency & Memory Profiling**
     - Run a memory profiling tool (like `mprof` from the `memory_profiler` package or Python's built-in `tracemalloc`) on the pre-existing data processing script `/app/data_processor.py`. 
     - Capture the peak memory usage in MiB.
     - Write a report to `/home/user/build_artifacts/memory_report.txt` containing strictly the peak memory usage as a float (e.g., `45.21`).
     
     **Stage C: Response**
     - If all steps succeed, return an HTTP 200 with the JSON response `{"status": "success", "target_version": "X.Y.Z"}` (replacing X.Y.Z with the parsed version).

Run the server in the background once it is ready so it can be evaluated. Be sure to handle any necessary path creations (like `/home/user/build_artifacts/`).