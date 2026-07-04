You are a data engineer tasked with building a real-time data extraction and serving pipeline. You have been provided with a video file containing a news broadcast with embedded subtitles and visual telemetry. 

The video file is located at `/app/broadcast.mp4`.

Your objectives are:
1. **Feature Extraction**: Extract frames from the video at exactly 1 frame per second (fps). For each extracted frame, calculate its average grayscale brightness (a value between 0 and 255).
2. **Structured Information Extraction**: Extract the embedded subtitle track (stream 0:s:0) from the video into SubRip (.srt) format. The subtitles contain multi-language text (including Unicode characters like Japanese/Chinese) formatted as: `[MSGID: <id>] Source: <name> - Payload: <text>`.
3. **Data Fusion**: Correlate the data. For each second `T` (0, 1, 2, ...), find the corresponding frame's brightness and the subtitle text that is active during that exact second.
4. **Template Generation**: Create a Go text template to generate a summary report of the data. The report should list each second, its brightness (rounded to 2 decimal places), and the extracted `<text>` payload.
5. **Data Serving**: Write and run a Go HTTP server listening on `127.0.0.1:8080` with the following endpoints:
   - `GET /api/data?sec=<T>`: Returns a JSON object for second `T`. Format: `{"second": <T>, "brightness": <brightness_value>, "payload": "<text>"}`. If no subtitle is active at second `T`, payload should be an empty string.
   - `GET /report`: Returns the generated text summary using your Go template. The format per line should be: `Sec <T>: Brightness <brightness>, Payload: <text>`.

Requirements:
- You must write the main extraction, aggregation, and server logic in **Go**.
- You may use standard CLI tools like `ffmpeg` to extract frames and subtitles, which your Go program can call or process the outputs of.
- Ensure your HTTP server runs continuously in the background or foreground so that it can be verified.
- Ensure Unicode characters are properly handled and served in the JSON and text endpoints.

Start your server on `127.0.0.1:8080`.