You are a platform engineer maintaining our CI/CD pipelines. We have a C++ data processing tool called `audioproc` located in `/home/user/audioproc`. This tool processes telemetry audio data (`/app/telemetry.wav`) collected from our server racks to detect acoustic anomalies. 

Currently, the CI pipeline is failing for several reasons:
1. **Memory/Lifetime Issues:** The tool crashes with segmentation faults due to dangling pointers and unsafe memory sharing in its naive implementation. 
2. **Performance:** The tool processes audio chunks sequentially. It is too slow to meet our CI pipeline SLA. 
3. **Schema Outdated:** The downstream database schema has been migrated. The tool currently outputs JSON in an old format, and it needs to be updated.

Your task is to fix and optimize this tool.

**Requirements:**
1. **Fix the C++ code:** Resolve all memory leaks and lifetime issues in `/home/user/audioproc/src/main.cpp` and `/home/user/audioproc/src/processor.cpp`. The code must compile and run cleanly without crashing.
2. **Concurrency:** Refactor the chunk processing to use a producer-consumer pattern with a thread-safe queue (conceptually similar to Go channels) using C++11/14/17 threading primitives. The main thread should read the WAV file and enqueue chunks, while a pool of worker threads calculates the RMS (Root Mean Square) volume for each chunk.
3. **Schema Migration:** Update the JSON output generation. 
   - Old schema format: `{"file": "/app/telemetry.wav", "chunks": [{"id": 0, "rms": 0.05}, {"id": 1, "rms": 0.12}]}`
   - New schema format: `{"metadata": {"source": "/app/telemetry.wav"}, "measurements": [{"chunk_index": 0, "rms_value": 0.05}, {"chunk_index": 1, "rms_value": 0.12}]}`
   (Note: Ensure chunk indices are correctly ordered in the final output despite concurrent processing).
4. **Build and Run:** Use CMake to build the project in `/home/user/audioproc/build`. 
5. **Output:** When executed as `./audioproc /app/telemetry.wav /home/user/output.json`, it must produce the correctly formatted JSON file.
6. **Performance:** The refactored concurrent processor must process the `/app/telemetry.wav` file in less than 200 milliseconds.

The audio file is already present at `/app/telemetry.wav`. Start by reviewing the source code in `/home/user/audioproc`, fix the compilation and runtime errors, implement the concurrent architecture, and verify the JSON output schema.