You are a security auditor tasked with securing a vulnerable custom file-processing web service. The original developer left behind an audio recording of a meeting where they discussed the exact security constraints needed for the service's input payloads, but they never implemented them. 

Your tasks are to:
1. Extract the audio from the file located at `/app/intercepted_dev_meeting.wav`. You will likely need to install a transcription tool (like `whisper-standalone` or use `ffmpeg` and external APIs if you prefer) to listen to or transcribe the contents.
2. Based on the rules described in the audio recording, implement a Python-based input sanitiser.
3. Write your solution to `/home/user/sanitiser.py`.
4. Your script must take exactly one argument: the absolute path to a JSON file containing the payload. Example: `python3 /home/user/sanitiser.py /path/to/payload.json`
5. The JSON payload will always have two keys: `"target_file"` (a string) and `"body"` (a string).
6. Your script must validate both fields against the rules mentioned in the audio recording.
7. If the payload is entirely benign and passes all rules, your script must exit with status code `0`.
8. If the payload violates ANY of the security rules (e.g., contains path traversal, XSS payloads, or unauthorized file extensions), your script must exit with status code `1`.

Make sure your script parses the JSON safely and handles missing keys or malformed JSON by exiting with code `1`. 

You are expected to produce a robust classifier. The automated test will run your script against two large corpora of JSON files: a "clean" corpus that must be accepted (exit 0) and an "evil" corpus full of malicious payloads that must be rejected (exit 1). Your solution must accurately classify both sets.