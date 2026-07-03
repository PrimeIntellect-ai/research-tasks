You are a security engineer analyzing a recent red-team exercise that targeted your organization's login flow via open redirect vulnerabilities.

We have recovered an intercepted audio file left by the red-team at `/app/voicemail.wav`, as well as an encrypted ZIP archive at `/app/evidence.zip`. 

Your tasks are to:
1. **Analyze the Audio:** Process `/app/voicemail.wav` to extract the spoken communication. The audio contains the password to unlock the `evidence.zip` archive, as well as specific instructions for hardening our SSH bastion.
2. **SSH Hardening:** Based on the exact port number and settings mentioned in the audio, create a hardened SSH configuration file at `/home/user/sshd_config_hardened`. (You do not need to restart the service, just produce the correct configuration file).
3. **Open Redirect Detector:** Extract the `evidence.zip` archive using the recovered password. Inside, you will find two directories containing text files (one URL per file):
   - `evil/`: Contains red-team open redirect evasion payloads.
   - `clean/`: Contains legitimate, safe redirect URLs used by our application.
   You must build a detection script at `/home/user/detector`. This script can be written in any language of your choice, but it must be an executable file (e.g., `chmod +x`). 
   - The script must read a single URL string from standard input (`stdin`).
   - If the URL is determined to be a benign local redirect (like the ones in the clean corpus), the script must terminate with **exit code 0**.
   - If the URL is determined to be malicious or an external open redirect (like the ones in the evil corpus), the script must terminate with **exit code 1**.

You may use any tools available in the environment to transcribe the audio (e.g., Python libraries like `SpeechRecognition` or system tools). Develop your filter carefully so that it correctly classifies 100% of the provided corpora without false positives or false negatives.