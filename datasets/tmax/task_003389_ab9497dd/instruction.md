You are acting as a performance engineer building a lightweight, high-performance acoustic data profiling tool. We have a raw audio signal artefact located at `/app/test_signal.wav` (which is a standard 44.1kHz, 16-bit, mono PCM WAV file) containing captured telemetry data.

We need a standalone C application that can parse this audio file, compute basic statistical and signal properties, and expose these metrics via a simple HTTP server for our scraping infrastructure.

Your task is to implement this application from scratch in C, compile it, and leave it running.

Requirements for the C application (`/home/user/workspace/analyzer.c`):
1. **Audio Parsing & Signal Processing:**
   - Read the WAV file at `/app/test_signal.wav`.
   - Skip the standard 44-byte WAV header.
   - Process the 16-bit integer PCM samples to compute two statistical metrics:
     a) `max_amp`: The maximum absolute amplitude value found in the signal.
     b) `zero_crossings`: The total number of times the signal crosses zero (i.e., when two consecutive samples have different signs; consider exactly 0 as a positive sign for this logic).

2. **HTTP Server Protocol:**
   - The program must start a TCP socket listening on `127.0.0.1:8000`.
   - It must accept incoming HTTP/1.0 or HTTP/1.1 requests.
   - When it receives a `GET /metrics` request, it must respond with an `HTTP/1.1 200 OK` status, a `Content-Type: application/json` header, and a JSON body containing the computed statistics.
   - Format of the JSON body: `{"max_amp": <integer>, "zero_crossings": <integer>}`
   - Any other path should return `HTTP/1.1 404 Not Found`.

3. **Performance Profiling:**
   - The server must compute the processing time taken *just for the audio parsing and metric calculation* (using `clock_gettime` or similar).
   - It must include an HTTP header in the response: `X-Process-Time-Us: <microseconds>`

4. **Workflow:**
   - Create the directory `/home/user/workspace`.
   - Write the C code to `/home/user/workspace/analyzer.c`.
   - Compile it using `gcc -O3 -o analyzer analyzer.c`.
   - Write a test script `/home/user/workspace/test.sh` that uses `curl` to query the server and print the response to stdout.
   - Execute the compiled `analyzer` binary in the background so that it is actively listening on port 8000 when you finish the task.

Do not use any external C libraries other than the standard library (libc). You must implement the WAV parsing and HTTP string formatting manually. Make sure the server runs continuously and handles multiple sequential requests.