You are an incident responder investigating a series of web server breaches. The attackers deployed several malicious CGI binaries to the web server to maintain persistence. 

During the investigation, you recovered an intercepted VoIP call recording located at `/app/voicemail.wav` and an encrypted archive of the suspected CGI binaries at `/app/evidence.zip`.

Your task is to:
1. Analyze the audio file `/app/voicemail.wav` to extract the password spoken in the recording. 
2. Use this password to extract `/app/evidence.zip` into `/home/user/evidence/`.
3. Write a Bash script at `/home/user/scan_cgi.sh` that acts as an automated vulnerability scanner for these ELF binaries. 

The script `/home/user/scan_cgi.sh` must:
- Take a directory path as its first argument (e.g., `/home/user/evidence/`).
- Safely analyze all files in the given directory. Since some binaries might be malformed or traps, you must use standard CLI tools (`readelf`, `objdump`, `strings`) rather than executing them or using unsafe tools like `ldd`.
- Identify binaries that are malicious/vulnerable based on the following criteria:
  a) It is a valid 64-bit ELF executable.
  b) It dynamically imports the `system` or `popen` function (check dynamic symbols).
  c) It contains the plaintext string `HTTP_USER_AGENT` (indicating it processes web requests).
- Print the basenames of the identified malicious binaries to `stdout`, one per line.

Your script will be evaluated against a hidden, held-out dataset of hundreds of CGI binaries. The verification system will run your script on this hidden dataset and compute the F1 score of the malicious binaries identified compared to the ground truth. To pass, your script must achieve an F1 score of >= 0.95 and process the directory efficiently.