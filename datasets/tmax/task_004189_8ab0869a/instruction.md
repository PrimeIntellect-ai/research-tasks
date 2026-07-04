As a localization engineer, I need to prepare assets for a new software release. We have a reference video with embedded subtitles, and we also need a robust stream processor for live translation logs.

Please perform the following two steps:

**Step 1: Extract Subtitles from Video**
There is a reference video at `/app/reference_video.mp4`. It contains an embedded subtitle track (stream 0:1). Extract this subtitle track and save it exactly as `/home/user/reference.srt`. 

**Step 2: Create a Stream Processor for Transcription Logs**
We receive massive, continuous streams of transcription logs that need to be converted into XML templates for our translation memory system. 
Write a Python script at `/home/user/stream_parser.py` that reads from `stdin` line-by-line (to support large-file streaming without running out of memory) and writes to `stdout`.

Each line in the log *should* follow this exact format:
`HH:MM:SS.mmm - <SPEAKER_ID> : RAW_TEXT`
Where:
- `HH:MM:SS.mmm` is a timestamp (digits only for time components, exact lengths: 2 for HH, MM, SS, and 3 for mmm).
- `SPEAKER_ID` is strictly uppercase letters and numbers, between 2 and 10 characters long.
- `RAW_TEXT` is the rest of the line (can contain any characters).

You must use a regular expression to parse each line.
For every line read from standard input:
- If it strictly matches the format, use template-based text generation to print exactly:
  `<trans unit="SPEAKER_ID" time="HH:MM:SS.mmm">RAW_TEXT</trans>`
- If it does not match the format (e.g., missing spaces, invalid timestamp, wrong speaker ID format), print exactly:
  `<error>MALFORMED</error>`

Trailing newlines from `stdin` should be stripped before processing, and each output XML/error string should be printed on its own line. Your script must be precise and match the required format perfectly.