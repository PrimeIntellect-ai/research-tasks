You are an automation specialist managing a custom data processing pipeline. We have a legacy C-based TCP server located at `/home/user/server.c` that acts as a microservice in our workflow. 

The server is supposed to listen on `127.0.0.1:7777`. When it receives a JSON-like line over a TCP connection (e.g., `{"text": "Signal \\u03B1"}\n`), it must:
1. Parse the text and decode any Unicode escape sequences (e.g., `\u03B1` to the UTF-8 character `α`).
2. Read the audio file located at `/app/audio.wav` (which is a standard 16-bit signed PCM WAV file) and compute the maximum rolling sum of the absolute values of the 16-bit samples using a window size of 500 samples. (Skip the 44-byte WAV header).
3. Respond with a JSON-line containing the decoded text and the computed maximum sum: `{"decoded": "Signal α", "max_sum": <integer>}\n` and close the connection.

Currently, the server code has not been written or is incomplete. Your task is to write or complete `server.c` to fulfill these requirements. 

Requirements:
- The server must handle basic `\uXXXX` to UTF-8 conversion.
- Calculate the rolling sum of the absolute sample values (16-bit signed integers, little-endian) from `/app/audio.wav`. Use a window size of exactly 500 samples.
- Compile the code to `/home/user/server` using `gcc`.
- Run the server in the background so it listens on `127.0.0.1:7777`.
- Do not use external libraries other than standard C libraries (e.g., no `libjansson`, just basic string searching is fine for the simplified JSON format expected).

Once the server is compiled and running in the background, your task is complete.