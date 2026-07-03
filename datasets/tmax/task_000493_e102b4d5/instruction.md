You are acting as a security auditor investigating a recent breach. Our intrusion detection system flagged anomalous activity, and we intercepted a voicemail from a compromised employee. 

Your objectives are as follows:

1. **Transcribe the Audio Artifact:** 
   An intercepted audio file is located at `/app/voicemail.wav`. Transcribe the audio (you may install tools like `ffmpeg` or `whisper` if needed). The audio contains a spoken passphrase.

2. **Unlock and Investigate:**
   Use the extracted passphrase to decrypt the SSH private key located at `/home/user/.ssh/id_rsa`. Once decrypted, connect to the local mock-server at `ssh auditor@localhost -p 2222`. 
   
3. **Log Analysis and Corpus Generation:**
   On the server, you will find a directory `/var/log/proc_audits/`. Download these logs to your local machine. These logs contain snapshots of `/proc/[pid]/cmdline` and `/proc/[pid]/environ` for various executed processes. 

4. **Build an Anomalous Process Detector:**
   Write a Python script at `/home/user/detector.py` that classifies whether a given log file represents a security violation (specifically, a script leaking credentials via command-line arguments). 
   
   Your script must accept a directory path as its first argument and output a JSON dictionary mapping the filename to a boolean (True if it's a credential leak, False if it is benign).
   
   Execution format: `python3 /home/user/detector.py <path_to_corpus_directory> > /home/user/results.json`

   The system will automatically test your script against two hidden corpora:
   - `evil/`: Contains logs where credentials (passwords, AWS keys, API tokens) are visibly passed as command-line arguments instead of securely via environment variables or files.
   - `clean/`: Contains normal system process logs, or processes where credentials are securely passed via environment variables.

Your script must correctly flag 100% of the `evil` logs and preserve (flag as False) 100% of the `clean` logs.