You are an AI assistant acting as a data engineer. We are building a real-time ETL pipeline for a video livestream platform. Your task is to extract configuration from a video file and implement a stream-processing TCP server in C.

Here are the requirements:

1. **Video Analysis & Setup**
   - You are provided a video file at `/app/stream.mp4`.
   - Use standard command-line tools to find the video's average frame rate (FPS). Round this to the nearest integer. Let this value be `N`.
   - Create a file at `/home/user/video_stats.txt` containing exactly this integer `N` followed by a newline.

2. **Stream Processing Server (C)**
   - Write a C program at `/home/user/server.c` and compile it to `/home/user/server`.
   - The server must listen for TCP connections on `127.0.0.1:9000`.
   - It should accept a stream of line-terminated (`\n`) text messages.
   - For every incoming message, the server must:
     a) Count the number of valid Unicode code points (characters) in the message (excluding the newline).
     b) Maintain a rolling window of the code point counts of the last `N` messages received across the entire lifetime of the server (using the `N` calculated in step 1).
     c) Calculate the sum of the code point counts in this rolling window.
     d) Immediately reply to the client with this sum as an integer string followed by a newline (`\n`).
     e) Append a log entry to `/home/user/pipeline.log` in the format: `RECV: <codepoint_count> | WINDOW_SUM: <sum>\n`.

3. **Execution**
   - Leave your server running in the background listening on port 9000 before completing your turn.

*Hint for UTF-8 in C*: A standard way to count Unicode code points in a UTF-8 string is to count all bytes that do not match the binary pattern `10xxxxxx` (i.e., bytes where `(byte & 0xC0) != 0x80`).

Ensure your code handles multiple subsequent messages correctly and operates as a long-running daemon.