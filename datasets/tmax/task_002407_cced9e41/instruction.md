You are an engineer tasked with setting up a highly secure, memory-efficient polyglot build system from scratch. You must complete the following phases:

**Phase 1: Architectural Extraction (Audio)**
Your lead architect left a recorded voice memo detailing critical configuration parameters for the build server. The audio file is located at `/app/architect_voicemail.wav`.
Transcribe this audio file. The transcript will reveal two crucial integers:
1. The PORT number the build server's WebSocket must bind to.
2. The absolute MEMORY_LIMIT in Megabytes that the server must not exceed under load.

**Phase 2: Patch Sanitization (Detector)**
The build system receives build configurations as standard unified diffs (patches). You must write a Python classifier that detects directory traversal and out-of-bounds file modifications. 
Create a script at `/home/user/patch_sanitizer.py` that takes exactly one argument (the path to a patch file).
- The script must exit with code `0` if the patch is perfectly safe (only modifies or creates files strictly within a theoretical `src/` directory, without escaping it).
- The script must exit with code `1` (and print a reason to stderr) if the patch is "evil" (contains absolute paths, references to `../` that escape the working directory, or touches hidden system directories like `.git/`).
*Note: Your sanitizer will be tested against a hidden corpus of clean and evil patches.*

**Phase 3: WebSocket Build Server & Memory Profiling**
Write the main server code at `/home/user/build_server.py`.
- It must host a WebSocket server on `ws://127.0.0.1:<PORT>` (using the port from Phase 1).
- When a client sends a patch payload as a text string, the server must write it to a temporary file, run `/home/user/patch_sanitizer.py` on it, and if it exits `0`, simulate applying the patch (you can just print "Applied").
- You must integrate memory profiling (e.g., using Python's `tracemalloc`).
- Create a benchmarking script `/home/user/benchmark.py` that sends 100 WebSocket messages (mix of safe and unsafe patches) to the server.
- The server must output its peak memory usage during the benchmark to `/home/user/memory_report.log` in the format: `Peak Memory: <X> MB`. The value `<X>` must be strictly less than the `<MEMORY_LIMIT>` extracted from the audio in Phase 1.