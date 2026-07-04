You are a forensics analyst investigating a compromised smart-home voice assistant server. The attacker managed to achieve remote code execution through a malicious audio payload that exploited a command injection vulnerability in the voice-to-text processing pipeline.

Your mission involves two main objectives: Evidence Recovery and Exploit Mitigation.

**Phase 1: Evidence Recovery**
1. An audio file containing the attacker's payload has been recovered at `/app/evidence/payload.wav`.
2. You must transcribe the hidden payload from this audio file. You may use any available tools (like `whisper` or `ffmpeg` pipelines) to recover the spoken command.
3. Once you have the transcription, parse the server logs located at `/app/logs/voice_assistant.log`. Find the entry that matches the transcribed command to identify the attacker's IP address.
4. Create a final report at `/home/user/forensics_report.json` with the following exact structure:
```json
{
  "transcription": "<exact_transcribed_text_in_lowercase>",
  "attacker_ip": "<extracted_ip_address>"
}
```

**Phase 2: Exploit Mitigation**
The vulnerability occurred because the server directly executed shell commands interpolated with the transcriptions. The engineering team is fixing the sink, but they need an immediate Web Application Firewall (WAF) equivalent for text transcripts to block further exploitation.

1. Create a script at `/home/user/sanitizer` (it must be executable, e.g., `chmod +x /home/user/sanitizer`). You can write it in any language (Python, Bash, etc., using a shebang).
2. The script must take exactly one argument: the absolute path to a text file containing a single voice command transcription.
   * Example invocation: `/home/user/sanitizer /tmp/input.txt`
3. The script must output exactly the word `ALLOW` or `BLOCK` to standard output (with a newline), based on whether the transcription contains malicious shell injection attempts (e.g., pipes, redirects, backticks, curl/wget commands) or is a benign voice command.
4. We have provided a test suite of transcripts. Your sanitizer must correctly output `ALLOW` for all files in `/app/corpora/clean/` and `BLOCK` for all files in `/app/corpora/evil/`.

You have complete freedom in how you write the sanitizer, as long as it handles the provided corpora with 100% accuracy.