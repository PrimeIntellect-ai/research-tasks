As a compliance analyst, you are investigating a recent security incident. We have a screen recording of the attacker's terminal session during the breach, located at `/app/incident_record.mp4`. The video shows the attacker crafting an exploit payload, configuring a local firewall bypass, and running a script to audit and abuse privilege escalation vectors.

Your task consists of two parts:

1. **Video Analysis and Audit Trail Generation**:
   Extract frames from the video at `/app/incident_record.mp4` to identify the exact exploit payload string used by the attacker. Look for a base64 encoded string passed to a vulnerable service. Once you find it, create an audit log file at `/home/user/audit_trail.txt` containing exactly the decoded payload string on the first line, and the firewall rule command the attacker used on the second line.

2. **Payload Classifier Creation**:
   Based on your analysis of the exploit payload, build a payload detection script. You must write a script (in any language you choose) located at `/home/user/payload_classifier.sh` (or `.py`, `.js`, etc., but make sure it is executable and has the correct shebang).
   This script will be tested against two directories of payloads:
   - `/app/corpora/evil/`: Contains files with malicious payloads similar to the one in the video.
   - `/app/corpora/clean/`: Contains files with benign compliance logs and regular service inputs.
   
   Your script must take a single argument (the path to a file) and exit with code 1 if the file contains a malicious payload (reject), and exit with code 0 if the file is benign (preserve).

Ensure your classifier is highly accurate, as it will be graded against an unseen adversarial corpus using the same structure.

Output the path to your executable classifier script in `/home/user/classifier_path.txt`.