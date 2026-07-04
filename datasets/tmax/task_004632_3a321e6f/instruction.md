As a red-team operator, you are analyzing a custom evasion tool used by an advanced threat actor to bypass an intrusion detection system (IDS) and Web Application Firewall (WAF). You have extracted a stripped ELF binary located at `/app/waf_evasion_encoder`. 

This binary takes a single raw payload string as a command-line argument and outputs an encoded payload equipped with an authentication token (which acts as a signature to bypass the WAF). 

Your objective is to reverse-engineer the behavior of this black-box binary (you may use tools like `strings`, `ltrace`, `strace`, or simply analyze its input/output behavior) and perfectly recreate its logic in a standalone Bash script. 

You must create the script at `/home/user/craft_payload.sh`. 
The script must:
1. Accept exactly one argument (the raw payload string).
2. Print the exact same evasion payload format to standard output as the `/app/waf_evasion_encoder` binary does for any given input.
3. Be written primarily in Bash (using standard Linux utilities like `awk`, `sed`, `xxd`, `sha256sum`, `base64`, `rev`, etc.).

Ensure your script is executable (`chmod +x /home/user/craft_payload.sh`). Your implementation must be bit-for-bit identical in output to the provided binary for any printable ASCII string input up to 200 characters.

Do not use hardcoded outputs for specific inputs; you must implement the actual underlying algorithmic transformations and token generation logic.