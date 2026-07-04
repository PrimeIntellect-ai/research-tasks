You are a build engineer responsible for recovering and integrating a legacy audio processing and encoding pipeline. The pipeline consists of a C shared library, a Go REST API, and a Bash client. Currently, the build is broken, the API is unstable under load, and the C code has memory safety issues. 

Your objectives are as follows:

1. **Extract Metadata:** There is an audio voicemail from the lead architect located at `/app/voicemail.wav`. Use available transcription tools (like `whisper` or `ffmpeg` combined with a Python script) to extract the "secret multiplier" mentioned in the audio.

2. **Fix the C Shared Library:** In `/home/user/workspace/lib/process.c`, there is a function `char* encode_string(const char* input, int multiplier)`. It currently has a buffer overflow vulnerability if the input string exceeds 10 characters. Fix the C code so that it safely truncates any input to a maximum of 10 characters before processing, without leaking memory or crashing. Compile it into a shared library named `libprocess.so`.

3. **Fix the Go API:** In `/home/user/workspace/api/server.go`, there is a Go-based REST API that uses CGO to call `encode_string` from `libprocess.so`. It suffers from a concurrency bug where multiple goroutines accessing the `/compute` endpoint share a global buffer, causing race conditions. Refactor the Go code to be thread-safe (e.g., using channels or local allocations), compile it, and start the server on port 8080.

4. **Create the Client:** Write a Bash script at `/home/user/query.sh` that takes exactly one command-line argument (an input string). The script must use `curl` to send a GET request to `http://127.0.0.1:8080/compute?input=<arg>&multiplier=<secret_multiplier>`. The script must parse the JSON response and print *only* the raw string value of the `"result"` field to standard output. 

Ensure `/home/user/query.sh` is executable (`chmod +x`). Once you have the Go server running in the background and the `query.sh` script fully functional, you have completed the task. Automated systems will test your `query.sh` script against a reference oracle with hundreds of random inputs.