You are acting as a network engineer inspecting a recent security incident. Our voice-activated router management system was compromised. We discovered that a background script was leaking session tokens via command-line arguments visible in `/proc`, which the attacker used to craft malicious voice commands containing XSS and command injection payloads.

We have intercepted the attacker's audio payload and captured a dataset of subsequent network logs.

Your objectives:
1. **Analyze the Audio Fixture**: There is an intercepted audio file at `/app/intercepted_command.wav`. Transcribe and analyze this audio. It contains the exact spoken command injection payload the attacker used.
2. **Reverse Engineer the Binary**: Analyze `/app/router_mgr.elf` to understand how it processes these voice-transcribed inputs and where the injection vulnerability lies. Verify its integrity against the checksum in `/app/checksums.txt`.
3. **Build a Detector**: Write a classifier script at `/home/user/detector.py` that takes a single file path as a command-line argument. The file will contain one transcribed network log entry per line. Your script must print `EVIL` to stdout for lines containing the XSS/Command injection patterns identified from the audio and binary analysis, and `CLEAN` for benign lines. 

Your `detector.py` must perfectly distinguish between malicious and benign inputs based on the specific injection vectors targeting `router_mgr.elf`. We will run your script against our internal test corpora.