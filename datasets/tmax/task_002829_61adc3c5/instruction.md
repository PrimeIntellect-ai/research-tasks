You are a penetration tester investigating a recent system breach. We have two main tasks for you involving forensic analysis of intercepted artifacts.

**Part 1: Video Forensics**
We intercepted a screen recording of the attacker's terminal during the breach. The video file is located at `/app/capture.mp4`. During the recording, the attacker accidentally executed a command that flashed their secret exfiltration token on the screen for a fraction of a second. 
Your task is to extract the frames, locate the token (which is exactly formatted as `TOKEN:<16-character-alphanumeric-string>`), and save the entire token string to `/home/user/video_secret.txt`. You may use `ffmpeg` and OCR tools (like `tesseract`, which you can install if needed) to assist you.

**Part 2: Payload Classification (Adversarial Corpus)**
The attacker interacted with our systems via SSH, and we have recovered several session transcripts. We need an automated way to detect malicious payloads (specifically, obfuscated command injections and reverse shell attempts) in these transcripts.
We have provided a training/validation dataset:
- Known malicious transcripts: `/app/corpus/evil/`
- Known benign transcripts: `/app/corpus/clean/`

You must write a classifier script, located at `/home/user/detector.py` (or `.sh`, `.js`, etc., as long as it is executable and accepts arguments). 
- The script must take a single command-line argument: the path to a directory containing transcript files.
- For every file in the specified directory, the script must print a single line to standard output in exactly this format: `<filename>: EVIL` or `<filename>: CLEAN`.
- Your script must successfully identify all malicious files (which contain CWE-78 OS Command Injection techniques like `base64 -d | sh`, `nc -e`, or anomalous `eval` usage) while preserving benign administrative sessions.

Your script will be tested by an automated verifier against both the provided clean/evil corpora and an unseen, hidden test set. Ensure your detection logic is robust.