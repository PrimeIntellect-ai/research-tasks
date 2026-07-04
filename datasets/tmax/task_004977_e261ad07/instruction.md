You are tasked with setting up a polyglot build system and exposing its outputs via a web service. 

We have received an audio transmission, located at `/app/signal.wav`, which contains a sequence of standard DTMF (Dual-Tone Multi-Frequency) tones. We also have two base64-encoded data files: `/app/data_A.b64` and `/app/data_B.b64`.

Your objectives are:

1. **Decode the Audio**: Analyze `/app/signal.wav` to extract the sequence of digits encoded as DTMF tones.
2. **Minimal Assembly Library**: Write an x86_64 assembly file that defines a single global function `get_code()`. This function must return the integer value of the decoded DTMF sequence. Compile and link this assembly file into a shared library named `/home/user/libcode.so`.
3. **Data Processing**: Read both `/app/data_A.b64` and `/app/data_B.b64`. Decode their base64 contents into plain text. Merge the lines from both files, sort them alphabetically in ascending order, and remove any duplicate lines.
4. **Python Web Service**: Write a Python script to start an HTTP server listening on `127.0.0.1:8888`. You may use Python's built-in libraries or lightweight frameworks like Flask. The server must implement two endpoints:
   - `GET /api/code`: Load `/home/user/libcode.so` using `ctypes`, call `get_code()`, and return a JSON response in the format `{"code": <integer_value>}`.
   - `GET /api/data`: Return the merged and sorted data lines as a JSON array in the format `{"data": ["line1", "line2", ...]}`.

The service must remain running in the foreground or background so that automated tests can query these endpoints. Please leave the server running when you consider the task complete.