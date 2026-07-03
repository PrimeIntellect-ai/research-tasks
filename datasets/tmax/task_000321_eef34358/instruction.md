We have intercepted an audio recording of a red-team briefing, located at `/app/redteam_briefing.wav`. The audio outlines a specific set of evasion techniques the red team is using against our JWT authentication system. 

Your objective is two-fold:
1. Transcribe or analyze the audio file to determine exactly which JWT vulnerabilities the red team is exploiting (e.g., algorithm confusion, `alg=none` bypasses, or specific payload injections).
2. Write a Python script at `/home/user/jwt_filter.py` that acts as a robust filter to detect these evasion payloads.

Your script must accept exactly two command-line arguments: an input directory containing files with JWT tokens (one token per file), and an output log file.
Usage: `python3 /home/user/jwt_filter.py <input_directory> <output_log.json>`

For each file in the input directory, your script must determine if the JWT is clean or malicious based on the techniques discussed in the audio.
The output log must be a JSON dictionary mapping the filename to a boolean indicating whether it is malicious (`true` for malicious/evil, `false` for clean).
Example `output_log.json`:
```json
{
  "token1.txt": false,
  "token2.txt": true
}
```

To help you test, a sample corpus is provided:
- `/app/corpus/clean/`: Contains legitimate tokens.
- `/app/corpus/evil/`: Contains red-team payloads.

Ensure your filter perfectly discriminates between the two without modifying any file permissions, and verify that it strictly detects the methods mentioned in the audio. Automated tests will run your script against a hidden verification corpus.