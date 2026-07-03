You are acting as a Localization Engineer. We have received a new batch of audio dialogues for an upcoming software release. The raw audio is located at `/app/dialogue_raw.wav`. 

Your goal is to transcribe this audio, clean the data, bucket it by time, and serve it via a custom C-based TCP service so that our downstream translation API can query it.

Here are your specific instructions:

1. **Transcription (Feature Extraction):**
   - You need to transcribe the spoken content in `/app/dialogue_raw.wav`.
   - Clone the official `whisper.cpp` repository (from ggerganov) to `/home/user/whisper.cpp`, compile it, and download the `ggml-base.en.bin` model.
   - Run the audio through the tool to generate a CSV or VTT output that includes timestamps.

2. **Data Cleaning, Normalization, and Time-based Bucketing:**
   - Extract the text and timestamps.
   - Clean the text: convert everything to lowercase, remove all punctuation (except spaces), and remove any duplicate phrases within the same bucket.
   - Aggregate the text into 10-second buckets based on the start time of the spoken segment (Bucket 0: 0.000s to 9.999s, Bucket 10: 10.000s to 19.999s, Bucket 20: 20.000s to 29.999s, etc.).
   - If a bucket has multiple segments, concatenate them with a single space.

3. **C-based Data Server (Integration & Validation):**
   - Write a C program at `/home/user/loc_server.c` that parses your cleaned, bucketed data.
   - The program must act as a TCP server listening on `127.0.0.1:9090`.
   - Protocol: 
     - The client connects and sends a newline-terminated string representing the bucket start time (e.g., `10\n` for the 10-19.999s bucket).
     - The server must respond with the cleaned text for that bucket, followed by the localization tag ` [LOC-EN]\n` (note the leading space), and then close the connection.
     - If the bucket has no data or doesn't exist, the server should respond with `EMPTY [LOC-EN]\n`.
   - Compile this C code using `gcc` and leave the server running in the background.

Please complete all steps and leave the TCP server running on port 9090.