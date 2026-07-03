As an automation specialist, you are tasked with building a highly specific text-processing microservice in C. 

We have an audio recording located at `/app/config_audio.wav`. This audio contains a spoken configuration for your service, specifically detailing the TCP port your service should listen on, and the rolling window size `W` it should use for aggregation. 
You must first transcribe this audio (you may use Python's `SpeechRecognition` library with `pocketsphinx`, or any available tools) to discover the port number and the window size.

Once you have the configuration, write a C program that acts as an HTTP server. 
The server must meet these requirements:
1. Listen on `127.0.0.1` at the port specified in the audio.
2. Accept `POST` requests to the endpoint `/aggregate`.
3. The HTTP request body will contain a space-separated sequence of ASCII words.
4. Your C program must process this text by applying a rolling window of size `W` (where `W` is the window size from the audio) over the sequence of words.
5. For each window, use a hash-based deduplication approach to count the number of strictly unique words in that window.
6. The server must respond with an `HTTP/1.1 200 OK` response. The response body must be a JSON array of the unique counts for each window in order. For example, if `W=3` and the words are "apple banana apple cherry", the windows are ["apple", "banana", "apple"] (unique count: 2) and ["banana", "apple", "cherry"] (unique count: 3). The response body should be `[2, 3]`.

You must implement the HTTP parsing, the rolling aggregation, and the hash-based deduplication in C. You may write a basic HTTP parser that simply extracts the body based on the `Content-Length` header.
Compile your server to an executable named `/home/user/server` and run it in the background so it is actively listening.

Constraints & Notes:
- Keep the server running. An automated verifier will send real HTTP POST requests to your service to evaluate its correctness.
- Handle standard HTTP headers properly to read the full body.
- Assume maximum word length is 64 characters and maximum body size is 100KB.