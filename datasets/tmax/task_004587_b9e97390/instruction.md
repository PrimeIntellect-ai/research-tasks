Wake up, it's 3 AM. You are the on-call engineer. Our financial transaction processing backend just crashed due to a subtle timezone and floating-point bug, and we are being flooded with un-sanitized payloads. 

The automated pager system has left a diagnostic voice message containing the root cause analysis and the exact precision repair rules we need to implement.

Here is what you need to do:
1. Listen to the automated pager dictation located at `/app/pager_recording.wav`. You may use any available command-line audio tools or transcription utilities (like `whisper` or `ffmpeg`) to decode the message.
2. The dictation explains how malformed `tz_offset_hours` fields in our JSON payloads are causing the system to crash, and specifies the exact floating-point rounding and validation rules required.
3. Write a Python script at `/home/user/sanitizer.py` that implements this logic.
   - The script must take a single command-line argument: the path to a JSON file.
   - The JSON file will contain a dictionary with a `"tz_offset_hours"` key (a float).
   - The script must read this file, apply the floating-point precision repair and validation logic described in the audio, and determine if the payload is safe.
   - If the payload is safe (clean), the script MUST exit with status code `0`.
   - If the payload is malformed/unsafe (evil), the script MUST exit with status code `1`.

Your script will be tested against a massive corpus of both clean and adversarial payloads to ensure no invalid offsets poison the database and no valid data is dropped due to standard floating-point noise.