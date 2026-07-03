You are acting as a localization engineer working on a subtitle generation pipeline for a new app walkthrough video. 

Your task involves two parts:
1. **Video Analysis:** We have a reference video of the app walkthrough located at `/app/loc_reference.mp4`. The video consists of exactly 5 distinct scenes (solid color screens representing different parts of the app), separated by sharp cuts. Use `ffmpeg` (which is pre-installed) to analyze the video and determine the exact start and end timestamps (in milliseconds) of these 5 screens.

2. **Localization Processor (Go):** Write a Go program at `/home/user/loc_render.go` that reads localization data from standard input and generates a valid SRT subtitle file on standard output. 
   
   The input will be a stream of JSON Lines (JSONL). Each line represents a translation key for a specific screen:
   `{"screen_id": 1, "key": "btn_submit", "translation": "Enviar"}`
   *Note: `screen_id` will be between 1 and 5.*

   Your Go program must:
   - Read all JSONL records from standard input.
   - Group the records by `screen_id`.
   - Sort the records within each screen alphabetically by `key`.
   - Handle Gap-filling: If any screen (from 1 to 5) has NO records provided in the input, you must automatically inject a default record: `{"key": "DEFAULT", "translation": "Missing"}` for that screen.
   - Generate an SRT formatted output using the exact timestamps you extracted from `/app/loc_reference.mp4`. 
   
   The SRT text block for a screen should be formatted exactly as follows:
   ```
   Screen <ID>:
   - <Key1>: <Translation1>
   - <Key2>: <Translation2>
   ```

To pass, your Go program must perfectly match the output of our internal reference implementation (`/app/oracle_render`) across a battery of random fuzz-tests.

**Constraints:**
- Use standard Go libraries only.
- Output strictly standard SRT format (timestamp format: `HH:MM:SS,mmm`).
- The output must be perfectly bit-for-bit identical to the oracle, so ensure your sorting, SRT index numbering (starting at 1), and newline formatting follow SRT conventions exactly.