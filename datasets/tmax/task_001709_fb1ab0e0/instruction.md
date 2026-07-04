You have just joined an incident response team and inherited an unfamiliar audio forensics codebase located at `/app/audio_pipeline/`. This multi-language pipeline (Python with a C extension for fast binary parsing) is used to extract hidden steganographic watermarks from `.wav` files. 

Recently, the pipeline has been failing in production. We suspect attackers are sending malformed or adversarial audio files that trigger a memory corruption or infinite loop in our C parsing extension. We have captured a specific payload that causes a crash, located at `/app/suspect_audio.wav`.

To help you test and debug, we have isolated an adversarial corpus and a clean corpus:
- `/app/corpora/clean/` contains 50 valid `.wav` files that the pipeline processes successfully.
- `/app/corpora/evil/` contains 50 adversarial `.wav` files that crash the pipeline.

**Your Objective:**
1. Comprehend the existing codebase in `/app/audio_pipeline/` to understand how it parses audio headers.
2. Perform binary diff analysis between the clean and evil files (and the suspect audio) to identify the specific structural anomaly triggering the vulnerability. 
3. Write a robust pre-filtering Bash script at `/home/user/detector.sh`.

**Detector Script Requirements:**
- The script must take exactly one argument: the absolute path to a `.wav` file.
- Example invocation: `/home/user/detector.sh /path/to/audio.wav`
- If the file is **clean**, the script must exit with status code `0`.
- If the file is **adversarial/evil**, the script must exit with status code `1`.
- The script should use standard bash built-ins, coreutils, or standard CLI tools (like `xxd`, `od`, `grep`, `awk`) to analyze the file and return the correct exit code quickly without actually running the vulnerable C code.
- You must ensure your detector achieves 100% accuracy on both provided corpora.