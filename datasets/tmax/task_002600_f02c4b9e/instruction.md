You are an automation specialist debugging a failed ETL job. The system recorded its data stream as an MP4 video, but due to a retry-loop bug, the data contains duplicate records.

The video artefact is located at `/app/etl_stream.mp4`. 
The video visually encodes a text stream: each frame represents a single bit of data. 
- If the frame's average grayscale luminance is strictly greater than 127, the bit is `1`.
- If the luminance is 127 or less, the bit is `0`.
- Every 8 consecutive frames form an ASCII character (Big-Endian / most significant bit first).

Your task is to build a processing pipeline to extract and clean this data:

1. **Feature Extraction (C Program 1)**: 
   Write a C program (e.g., `decode.c`) that reads raw 8-bit grayscale pixel data from standard input, calculates the frame-level bits, and decodes the ASCII characters. Use `ffmpeg` to pipe the video frames into your C program.

2. **Regex Parsing & Deduplication (C Program 2)**:
   The decoded text contains log entries separated by newlines. Due to ETL retries, many records are duplicates. 
   Write a second C program (`dedup.c`) that reads the decoded text. Use POSIX regex (`<regex.h>`) to parse each line. The format of valid lines is:
   `[<Timestamp>] ERROR_CODE:<Code> - <Message>`
   (e.g., `[1699991234] ERROR_CODE:500 - Database timeout`)
   
   Drop any line that does not strictly match this format.
   Deduplicate the records: If multiple records have the exact same `<Message>`, keep only the *first* occurrence (chronologically, based on order of appearance in the file).

3. **Output Generation**:
   The final output must be saved to `/home/user/clean_records.csv` with the headers: `Timestamp,ErrorCode,Message`.

You may use standard Linux shell tools and `ffmpeg` to glue your pipeline together, but the core decoding and regex/deduplication logic must be implemented in C.