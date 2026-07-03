You are a localization engineer setting up an automated translation pipeline for a new video game trailer. You need to extract text insertion timestamps from a reference video, sanitize crowdsourced translation files, and schedule the pipeline.

Your tasks are:

1. **Video Marker Extraction**:
   We use pure black frames (all pixels RGB 0,0,0) in our reference video to mark exactly where localized text cards should appear. 
   Analyze the video located at `/app/trailer.mp4`. Calculate the total number of pure black frames in the video. Save this integer count to `/home/user/card_count.txt`. You may use `ffmpeg` or write a Python script to extract and analyze the frames.

2. **Translation Sanitization**:
   Crowdsourced translations often contain formatting errors or malicious payloads. You must write a Python script `/home/user/sanitize.py` that validates translation files.
   
   The script must be invoked as: `python3 /home/user/sanitize.py <input_file> <output_file>`
   
   Input files contain one translation string per line.
   A valid (clean) translation string:
   - May contain standard game formatting tags: `<b>`, `</b>`, `<i>`, `</i>`, and `<color=#RRGGBB>...</color>`.
   - Must have properly matching open and close tags.
   - Must NOT contain any other HTML/XML tags (e.g., `<script>`, `<img>`, `<div>`, `<onload>`).
   - Must NOT contain unmatched tags or malformed tags.

   If a string is invalid/malicious, it must be completely excluded from the output file. Valid strings must be written to the output file exactly as they appeared.
   
   To help you develop this, we have provided two corpora:
   - `/app/corpora/clean/`: Contains files with only valid translations. Your script must preserve 100% of the lines in these files.
   - `/app/corpora/evil/`: Contains files with malicious or malformed translations. Your script must reject 100% of these lines.

3. **Pipeline and Scheduling**:
   Create a bash script `/home/user/run_pipeline.sh` that:
   - Writes the current timestamp to `/home/user/pipeline.log`.
   - Runs the video analysis and writes to `/home/user/card_count.txt`.
   - Runs your `sanitize.py` script on the staging file `/app/staging.txt`, writing the output to `/home/user/final_translations.txt`.
   
   Finally, configure a cron job for the `user` to execute `/home/user/run_pipeline.sh` every 5 minutes.