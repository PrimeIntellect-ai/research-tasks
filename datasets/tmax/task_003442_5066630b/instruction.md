You are acting as a data engineer helping a data scientist clean a messy time-series dataset. The data scientist has left you a voice memo in `/app/memo.wav` with some specific parameters for the pipeline.

Your objective is to write a standalone Rust CLI program that processes a corrupted JSON-Lines time-series dataset from `stdin` and writes the cleaned, aggregated data to `stdout`.

Requirements for the Rust program:
1. **Input Format:** Reads JSON-Lines from `stdin`. Each line has the schema: 
   `{"ts": <i64>, "note": "<string>", "val": <i64>}`
   *Note:* The `note` field contains text with raw unicode escape sequences (e.g., `\u00e9` for `é`).

2. **Character Encoding & Tokenization:**
   - Decode all unicode escape sequences in the `note` field to actual UTF-8 characters.
   - Tokenize the decoded string by whitespace.
   - For each token, remove all ASCII punctuation (characters `! " # $ % & ' ( ) * + , - . / : ; < = > ? @ [ \ ] ^ _ \` { | } ~`), then convert it to lowercase.
   - Discard any resulting empty tokens.
   - **Stop-word filtering:** Discard any tokens that match the exact stop-word specified in the `/app/memo.wav` audio file.

3. **Windowed Aggregation:**
   - Compute a rolling sum of the `val` field over the last `W` records.
   - The exact window size `W` is spoken in the `/app/memo.wav` audio file.
   - For the first `W-1` records, the rolling sum should just be the sum of all records seen so far.

4. **Output Format:** Writes JSON-Lines to `stdout`. Each line must have the schema:
   `{"ts": <i64>, "tokens": ["<string>", ...], "rolling_sum": <i64>}`

You must compile your finished Rust program to a binary located exactly at `/home/user/pipeline`.

*Hint:* You may need to use tools like `ffmpeg` or install a Python transcription library (like `SpeechRecognition` or `whisper`) to discover the hidden parameters in `/app/memo.wav`.