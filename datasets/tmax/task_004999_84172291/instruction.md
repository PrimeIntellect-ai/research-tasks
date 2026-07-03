You are a web security script developer tasked with creating a robust input sanitization utility for a voice-to-text web application. Recent incidents have shown that attackers are submitting audio files containing malicious payloads (like SQL injection and XSS disguised in spoken words) to compromise our backend.

Your objective has four phases:

1. Environment & Package Setup:
Create a working directory at `/home/user/voice_sec`. Initialize a Python virtual environment here and install `pytest`.

2. The Adversarial Classifier:
Write a Python module at `/home/user/voice_sec/sanitizer.py` containing a function with the signature:
`def is_safe_input(transcribed_text: str) -> bool`
This function must return `True` if the text is benign, and `False` if it contains web security threats (like XSS tags, SQL commands like DROP/SELECT mixed with typical injection syntax, or directory traversal sequences).

You must calibrate your function against our existing dataset. We have provided two directories:
- `/app/corpora/clean/` (contains `.txt` files with benign user voice notes)
- `/app/corpora/evil/` (contains `.txt` files with transcribed malicious voice injections)
Your function must correctly classify 100% of the files in both directories.

3. Testing Setup:
Write a test suite at `/home/user/voice_sec/test_sanitizer.py` using `pytest`. You must write test fixtures that dynamically load all files from the clean and evil corpora and assert that `is_safe_input` returns the correct boolean for every file.

4. Integration and Incident Analysis:
We recovered a suspicious audio file from a recent breach, located at `/app/incident_042.wav`. 
You must:
- Use the pre-installed system utility `whisper-stub` (a mocked transcription tool we placed in your path for this environment) to transcribe the audio file. Run: `/app/bin/whisper-stub /app/incident_042.wav > /home/user/voice_sec/incident_transcript.txt`
- Run your `is_safe_input` function on the resulting transcript.
- Create a final log file at `/home/user/voice_sec/incident_verdict.log`. The file must contain exactly one line: either `VERDICT: CLEAN` or `VERDICT: EVIL`.

Do not hardcode the verdicts; rely on your tested sanitizer.