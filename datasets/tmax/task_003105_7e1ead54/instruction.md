You are an incident responder investigating a potential supply chain attack affecting our web infrastructure. We have collected a set of suspicious ELF binaries from our servers, located in `/app/binaries/`. 

Recently, our Threat Intelligence team sent us a screenshot of an advisory containing known malicious IP subnets associated with this threat actor. The screenshot is located at `/app/threat_intel.png`.

Your objectives are:
1. Extract the malicious IP subnets (CIDR notation) from the image `/app/threat_intel.png`.
2. Write a Python script `/home/user/analyze.py` that statically analyzes all ELF binaries in `/app/binaries/`. 
3. For each binary, extract any IPv4 addresses hardcoded within its strings (e.g., in the `.rodata` or `.data` sections).
4. Determine which binaries contain at least one IP address that falls within any of the malicious subnets extracted from the threat intelligence image.
5. Your script must output a JSON file at `/home/user/flagged.json` containing a single list of the filenames (just the basenames, e.g., `["bin_01", "bin_42"]`) of the binaries that are flagged as malicious.
6. Additionally, your script should generate an iptables firewall script at `/home/user/block.sh` containing commands to drop outgoing traffic to the specific malicious IPs found in the flagged binaries. (Format: `iptables -A OUTPUT -d <IP> -j DROP`).

You may use standard Linux tools (like `strings`) or Python libraries (like `pytesseract` for OCR, `Pillow`, `lief` for ELF analysis, or the `ipaddress` module) as needed. 

An automated scoring system will evaluate your `flagged.json` file against the ground-truth list of malicious binaries by calculating the F1 score. You need to achieve an F1 score of at least 0.95 to pass.