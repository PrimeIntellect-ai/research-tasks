You are a security researcher investigating a suspicious Python script left behind by an attacker. You have recovered some logs from the compromised system and a partial decryption script (`/home/user/decoder.py`). 

Your objective is to reconstruct the timeline of the attack, fix the bugs in the decryption script, and decrypt the final payload.

1. **Log Timeline Reconstruction**
   There are three log files located in `/home/user/logs/`:
   - `firewall.log`
   - `auth.log`
   - `syslog`
   
   Analyze these logs to find the "Initial connection" event and the "Exec payload" event. The decryption key used by the malware is the exact time delta (in seconds) between these two events.

2. **Fix the Decoder Script**
   The script at `/home/user/decoder.py` is broken. It uses a recursive function to process the payload but fails to execute properly due to multiple bugs:
   - **Loop termination / Recursion fixing:** The recursive function never terminates and fails to progress through the data array, causing a `RecursionError`.
   - **Formula implementation correction:** The script currently attempts to decode bytes using the formula `(encrypted_byte ^ key) + (index % 256)`. However, reverse engineering of the malware binary confirms the correct formula should SUBTRACT the index modulo 256, i.e., `(encrypted_byte ^ key) - (index % 256)`. Ensure the resulting byte is properly masked to 8 bits (`& 0xFF`).

3. **Decrypt the Payload**
   Once the script is fixed, run it using the key you derived from the logs. Save the resulting decrypted text (the flag) exactly as it is outputted by the script into a file at `/home/user/flag.txt`. Do not include extra newlines or spaces.