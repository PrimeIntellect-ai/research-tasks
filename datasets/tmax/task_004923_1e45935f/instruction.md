You are a network security engineer tasked with inspecting captured network payloads and traffic logs. We have reason to believe that sensitive data and exploit attempts are being transmitted over our network. 

First, our team intercepted an internal VoIP call, saved at `/app/intercepted_call.wav`. You must transcribe this audio to discover the names of our three top-secret operational projects.

Second, you need to create a Python classifier that acts as a filter for our network inspection system. Write a script at `/home/user/classifier.py` that takes a single file path as a command-line argument. The script must read the contents of the file and determine if it is "clean" or "evil". 

A payload is considered "evil" (sensitive or malicious) if it contains:
1. Any mention of the three top-secret projects revealed in the audio (case-insensitive).
2. Any leaked SSH private keys (e.g., containing standard headers like `-----BEGIN OPENSSH PRIVATE KEY-----` or `-----BEGIN RSA PRIVATE KEY-----`).
3. Evidence of basic command injection or reverse shell payloads (specifically, any occurrence of the strings `nc -e`, `/bin/bash -i`, or `wget http` followed by execution).

Your script must exit with status code `1` if the file is "evil", and exit with status code `0` if the file is "clean".

To help you develop your script, we have provided a small sample corpus in `/home/user/sample_corpus/clean/` and `/home/user/sample_corpus/evil/`. However, your script will be evaluated against a hidden, much larger adversarial corpus. 

Requirements:
- Entry point: `python3 /home/user/classifier.py <filepath>`
- Ensure your script is robust and correctly handles standard text encodings.
- You may use any standard Python libraries or install tools like `whisper` or `ffmpeg` to process the audio.