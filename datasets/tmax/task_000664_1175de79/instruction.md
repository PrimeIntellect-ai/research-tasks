You are a network security engineer investigating a recent intrusion attempt on your company's internal diagnostic service. 

You have been provided with two files:
1. `/home/user/traffic.log`: A packet snippet containing an HTTP GET request intercepted by your firewall. The request contains an encoded malicious payload.
2. `/home/user/service.sh`: A local copy of the vulnerable Bash-based diagnostic service that the attacker was targeting.

Your objectives are:
1. **Analyze and Decode:** Inspect `/home/user/traffic.log` to find the attacker's payload. The payload is Base64 encoded inside the `data` query parameter. Decode it to determine which system file the attacker was attempting to read (using the `cat` command).
2. **Exploit Crafting:** You must prove the vulnerability by crafting your own exploit. Write a Bash script at `/home/user/exploit.sh`. 
3. When executed, your `exploit.sh` script must:
   - Generate a Base64-encoded payload.
   - Pass this encoded payload as the first argument to `/home/user/service.sh`.
   - The injected payload must cause `service.sh` to calculate the `sha256sum` of the file the attacker originally targeted, and write *only* the hash (the 64-character hex string, without the filename) to `/home/user/target_hash.txt`.

Constraints:
- You must write `/home/user/exploit.sh` and make it executable.
- Your exploit must work by passing the payload to `service.sh`, exploiting its command injection vulnerability. 
- Do not modify `service.sh` or `traffic.log`.
- `/home/user/target_hash.txt` should contain exactly the 64-character SHA-256 hash and a newline.