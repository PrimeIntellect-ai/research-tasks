You are a security auditor investigating a local privilege escalation incident on a Linux server. 

A custom C++ firewall management utility, located at `/home/user/fw_updater`, allows users to submit signed firewall rule manifests to open ports. You have been provided with the source code of the utility at `/home/user/fw_updater.cpp` and the application's audit log at `/home/user/fw.log`.

We suspect a vulnerability similar to the notorious "JWT algorithm=none" flaw, where the utility blindly trusts manifests if the signature algorithm is explicitly set to NONE.

Perform the following tasks:
1. **Log Analysis**: Parse `/home/user/fw.log` to identify the user who successfully exploited this vulnerability to bypass the signature check. Write ONLY their username to `/home/user/compromised_user.txt`.
2. **Binary Analysis**: Analyze the compiled ELF binary `/home/user/fw_updater` to find the virtual memory address of the string used to trigger the bypass (e.g., the exact string constant checking for "NONE" or similar as seen in the source code). Assume the binary was compiled without PIE (`-no-pie`). Write this address in standard hexadecimal format (e.g., `0x40201a`) to `/home/user/string_address.txt`. 
3. **Exploit Crafting**: Create a malicious manifest file at `/home/user/malicious.manifest` that exploits this vulnerability to apply the rule `ALLOW PORT 9999`. The file format must perfectly match what `fw_updater` expects to successfully parse and accept the bypass.

You may use standard shell tools (grep, awk, objdump, readelf, strings, etc.) to complete this task.