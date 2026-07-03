You are an open-source maintainer reviewing a pull request for an audio processing project called `audio-envelope-api`. 

The PR attempts to provide a REST API (using a Bash CGI script) that wraps a high-performance C shared library for extracting volume envelopes (RMS values in windows) from WAV files. However, the PR is completely broken and the original author has abandoned it. You need to fix it, get the API running, and successfully process a test audio file.

Here is the current state of the system in `/home/user/audio_pr`:
- `CMakeLists.txt`: Supposed to compile `src/envelope.c` into a shared library (`libenvelope.so`) and link it to a CLI executable `src/cli.c` (`envelope_cli`). 
- `src/envelope.c`: Contains the core logic. It has a function `float* compute_envelope(const char* filepath, int* out_length)` which calculates the RMS envelope of a WAV file.
- `src/cli.c`: A command-line tool that calls `compute_envelope` and prints a JSON array of the floats to stdout.
- `api/server.sh`: A Bash script that uses Python's `http.server` in CGI mode to serve a REST API on port 8080.
- `api/cgi-bin/process.sh`: The Bash CGI script that handles POST requests. It saves the POST body (a WAV file) to a temporary file, calls `envelope_cli`, and returns the JSON array.

**Your Tasks:**
1. **Fix the Build System & ABI:** The build is currently failing. `envelope_cli` complains about missing symbols at link time. Additionally, the project uses `-fvisibility=hidden` by default to manage the ABI, but the developer forgot to correctly export the `compute_envelope` function from the shared library. Fix `src/envelope.c` and `CMakeLists.txt` so that the project compiles and links successfully using standard CMake commands (build in a `build/` directory).
2. **Fix the Integration & API:** Make sure `api/cgi-bin/process.sh` properly invokes the compiled `envelope_cli`. You may need to modify the script to point to the correct path in the `build/` directory and ensure the shared library can be found at runtime (e.g., using `LD_LIBRARY_PATH`).
3. **Write an Integration Test in Bash:** Start the REST API server in the background. Write a Bash script `/home/user/run_test.sh` that makes an HTTP POST request using `curl` to `http://localhost:8080/cgi-bin/process.sh`, sending the binary contents of the audio fixture located at `/app/test_audio.wav`. 
4. **Output Generation:** The REST API must return a valid JSON array of floating-point numbers. Save this exact output to `/home/user/output.json`.

Ensure your integration test script handles the server lifecycle (starting it, waiting for it to be ready, sending the request, saving the output, and killing the server). 

The automated test will evaluate the numerical Mean Squared Error (MSE) between your `/home/user/output.json` and the ground truth envelope array. Ensure your JSON format is strictly a flat array of numbers: e.g., `[0.012, 0.054, 0.033, ...]`.