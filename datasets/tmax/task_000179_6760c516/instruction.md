You are a Linux systems engineer tasked with hardening our automated QEMU VM provisioning pipeline. We have had issues with malicious users submitting QEMU startup configurations that expose virtual machines to the public internet, misconfigure routing, or attempt to mount host filesystems to send spam emails.

Your objective is to create a robust Python script that acts as a gatekeeper, analyzing submitted QEMU bash scripts and rejecting those that violate our security policies.

First, the network security team has left an automated voicemail detailing the new strict hardening policies. You will find this audio file at `/app/voicemail.wav`. You must transcribe or listen to this file to understand the specific VNC and networking bridge requirements.

In addition to the rules in the voicemail, your script must also block any configurations that:
1. Attempt to use `-virtfs` or `-fsdev` to mount host directories.
2. Attempt to forward host port 25 (e.g., `hostfwd=tcp::25-:25`) which could be used for email server abuse.

We have provided a corpus of example QEMU configurations to test your script against:
- Safe configurations that should be allowed are located in `/app/corpus/clean/`.
- Malicious or misconfigured configurations that must be blocked are located in `/app/corpus/evil/`.

Write your validation script in Python at `/home/user/qemu_filter.py`. 
Your script must meet the following specifications:
- It must accept exactly one positional argument: the absolute path to a QEMU bash script to be analyzed.
- It must read and parse the provided file.
- If the file is deemed safe (complies with all rules), the script must exit with a status code of `0`.
- If the file is deemed malicious or non-compliant, the script must exit with a status code of `1`.
- It must handle missing files or read errors gracefully (exit code `1`).

You may use any tools (like `ffmpeg` or `whisper`) to analyze the audio file. Ensure your final script `/home/user/qemu_filter.py` correctly classifies all files in the provided corpus directories.