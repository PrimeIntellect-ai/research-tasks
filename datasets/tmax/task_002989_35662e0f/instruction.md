You are a network security engineer investigating a recent breach. Your team intercepted a suspicious audio transmission likely containing instructions from the threat actor regarding their post-exploitation toolkit and C2 infrastructure.

You have been provided with the intercepted audio file at `/app/intercepted_comms.wav`. 

Your objective is to:
1. Extract the threat indicators detailed in the audio recording. You may need to use tools like `whisper-cli`, `ffmpeg`, or similar audio/transcription utilities available in the environment to transcribe or analyze the audio.
2. Based on the extracted indicators, write a Bash script at `/home/user/threat_filter.sh`. 
3. This script will act as a classification filter for a large dataset of intercepted files and system artifacts.

The filter script must accept exactly one argument: the absolute path to a file to be analyzed.
`./threat_filter.sh /path/to/file`

The script must evaluate the file against the threat indicators from the audio:
- If the file is an **ELF binary**, it must check specific binary format properties, embedded strings, and file access permissions as dictated by the audio.
- If the file is a **text-based system log or script**, it must perform pattern matching to detect the specific service auditing or port scanning behavior described in the audio.

Exit Code Requirements:
- The script MUST exit with code `1` (reject) if the file matches the malicious criteria.
- The script MUST exit with code `0` (accept/preserve) if the file is benign.

Ensure your script handles varying file types gracefully and only flags files that strictly meet the adversary's exact criteria. Make the script executable (`chmod +x /home/user/threat_filter.sh`).