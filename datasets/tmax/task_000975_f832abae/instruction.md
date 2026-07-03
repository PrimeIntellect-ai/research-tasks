You are a Linux systems engineer tasked with hardening a server environment based on an urgent audio report from the Network Operations Center (NOC).

We have received a voicenote from the NOC at `/app/noc_report.wav` detailing a list of malicious IP addresses that are causing a network misconfiguration and need to be isolated. 

Your tasks are to:
1. Process the audio file `/app/noc_report.wav` to transcribe its contents and extract the malicious IP addresses mentioned.
2. Save the extracted IP addresses, one per line, to `/home/user/extracted_ips.txt`.
3. Write a Python script `/home/user/generate_fw.py` that reads `/home/user/extracted_ips.txt` and generates an idempotent bash script `/home/user/apply_firewall.sh`. 
4. The generated `/home/user/apply_firewall.sh` must use `iptables` to block inbound traffic from each extracted IP address. The script must be idempotent (running it multiple times should not create duplicate iptables rules).
5. The generated bash script must also use `expect` or text-processing pipelines to ensure that the rules are applied correctly and any interactive prompts from our legacy firewall auditing wrapper are bypassed (for the sake of this task, just ensure the `iptables` commands themselves are idempotent and properly formatted).

You may install any necessary Python packages (such as `SpeechRecognition`, `pydub`, `openai-whisper`) or system packages (like `ffmpeg`) to process the audio.

Your success will be evaluated based on the accuracy of the IP addresses extracted in `/home/user/extracted_ips.txt`.