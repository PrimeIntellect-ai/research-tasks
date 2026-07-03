You are acting as a Security Auditor responding to a recent breach. We have intercepted an attacker's audio memo, and we have collected samples of system logs. 

Your task is to analyze the audio, determine the specific attack indicators, and build a Rust-based log classifier to detect these attacks in our security logs.

Step 1: Audio Analysis
There is an audio file at `/app/auditor_notes.wav`. You must transcribe this audio file to uncover the exact vulnerability signatures the attacker used. The audio contains instructions detailing specific XSS payload structures and the exact ELF binary sections they are tampering with to bypass our integrity checks. (You may use Python packages like `SpeechRecognition` or `whisper` to transcribe the file, or any other tools available in the environment).

Step 2: Log Analysis
We have provided a training dataset of logs:
- `/app/corpora/clean/` contains benign JSON log files.
- `/app/corpora/evil/` contains malicious JSON log files representing the attacks described in the audio.

Each log file contains a JSON object representing either a web request or a file integrity check. Example format:
```json
{
  "timestamp": "2023-10-25T12:00:00Z",
  "event_type": "web_request",
  "data": {
    "url": "/search?q=hello",
    "headers": {"User-Agent": "Mozilla/5.0"}
  }
}
```
or 
```json
{
  "timestamp": "2023-10-25T12:05:00Z",
  "event_type": "elf_integrity",
  "data": {
    "binary_path": "/usr/bin/sshd",
    "tampered_section": ".text"
  }
}
```

Step 3: Rust Classifier Development
Create a Rust project at `/home/user/classifier`. 
Write a Rust program that takes a single command-line argument (the path to a JSON log file).
The program must parse the JSON log and:
- Exit with code `1` (Reject/Flag) if the log contains the specific XSS payloads or ELF tampering indicators mentioned in the audio and found in the evil corpus.
- Exit with code `0` (Accept/Clean) if the log is completely benign.

Requirements:
- The binary must be compiled in release mode: `/home/user/classifier/target/release/classifier`
- It must handle potentially malformed JSON gracefully (by rejecting it or safely ignoring, though the evaluation corpus will be valid JSON).

Your solution will be tested against a hidden, held-out evaluation corpus. You must achieve a 100% detection rate on the evil evaluation corpus and a 0% false positive rate on the clean evaluation corpus.