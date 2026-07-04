You are a storage administrator responsible for managing disk space on a legacy call-center archival server. We have a massive backlog of uncompressed WAV files taking up too much space. We need to implement a selective archiving script that only keeps the audio segments containing actual speech, discarding the long periods of silence or hold music, and compresses the result.

Your task is to write a Python script `/home/user/archive_audio.py` that processes a provided audio file `/app/call_record_001.wav` and its corresponding metadata file `/app/call_001_segments.txt`.

The segment file `/app/call_001_segments.txt` contains a list of timestamps and classifications in this format (tab-separated):
`[start_time_seconds] \t [end_time_seconds] \t [label]`
Example:
`0.00 \t 15.23 \t SPEECH`
`15.23 \t 45.10 \t HOLD_MUSIC`

Your script must:
1. Read the segment file and filter it to find only the lines labeled `SPEECH`. (You may use sed/awk or Python to process this).
2. Split the original `/app/call_record_001.wav` into temporary chunks corresponding strictly to the `SPEECH` segments.
3. Merge these speech chunks back into a single continuous WAV file.
4. Convert the merged WAV file to a 16kHz mono MP3 file at 32kbps to further save space.
5. The final output must be written to `/home/user/archived_call_001.mp3`. You must ensure atomic writes by writing the final MP3 to a temporary file first and then moving it to the final destination, avoiding corrupted states if the script is interrupted.

To verify your success, our automated system will transcribe your final MP3 file and compute the Word Error Rate (WER) against the ground-truth transcript of the original audio, as well as checking the final file size. 
Please ensure your script runs without user intervention and leaves the final MP3 file at `/home/user/archived_call_001.mp3`.