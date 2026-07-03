You are a localization engineer tasked with preparing translated subtitles for a product presentation video. Your upstream translation pipeline occasionally outputs malformed JSONL files, specifically corrupting or generating invalid Unicode escape sequences which crash the downstream subtitle renderer. You need to build a robust shell-based validation pipeline and then synchronize the valid translations with the video's scene changes.

This task involves two primary objectives:

### Objective 1: Create a JSON-Lines Validator / Sanitizer
Write a Bash script at `/home/user/validate_subs.sh` that takes a file path as its first argument and processes a JSONL file containing translations. 
Each valid line should be a JSON object with two keys: `"seq"` (integer sequence number) and `"text"` (translated string). 

Your script must:
1. Accept (print to stdout and exit with 0) valid JSONL lines.
2. Reject (print nothing for that line, exit with non-zero if the file contains any invalid lines) any lines that contain:
   - Malformed Unicode escapes (e.g., `\u` followed by less than 4 hex digits, or invalid hex).
   - Unpaired UTF-16 surrogate halves (e.g., `\ud800` not followed by a low surrogate).
   - Missing `"seq"` or `"text"` fields.
   - Values where `"seq"` is not a valid positive integer.
   
Note: You must implement this using purely Bash, coreutils, `jq`, `awk`, `sed`, or standard standard CLI tools (no Python/Node.js). 

We will test your script against a hidden suite of "clean" and "evil" translation files.

### Objective 2: Video Subtitle Synchronization
You are provided with a reference video at `/app/reference_ui.mp4`. The video contains discrete scene changes (slides transitioning). 
You must:
1. Extract the exact timestamps of scene changes from `/app/reference_ui.mp4` using `ffmpeg` (use a scene detection threshold of 0.3: `select='gt(scene,0.3)'`). The first slide starts at 0.000000.
2. Read the raw, unsanitized translation file provided at `/home/user/raw_translations.jsonl`.
3. Filter `raw_translations.jsonl` using your `validate_subs.sh` script to keep only the valid lines. 
4. Sort the valid translations by their `"seq"` number.
5. Map each ordered translation to a scene. The first translation corresponds to the video start (0.000000) until the first scene change. The second translation corresponds to the first scene change until the second scene change, and so on.
6. Enforce a windowed constraint: If a scene lasts longer than 5.0 seconds, the subtitle must disappear after exactly 5.0 seconds. 
7. Generate an SRT file at `/home/user/final_subtitles.srt` mapping the localized text to the correct timestamp windows (formatted as `HH:MM:SS,mmm`).

Provide all necessary scripts and the final `/home/user/final_subtitles.srt` file.