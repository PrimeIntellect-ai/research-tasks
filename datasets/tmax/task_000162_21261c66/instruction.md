You are a forensics analyst investigating a compromised host. 

You have been provided with two pieces of evidence:
1. A suspicious binary executable located at `/home/user/implant`. 
2. A log file containing Content Security Policy (CSP) violation reports from various internal machines, located at `/home/user/csp_violations.jsonl`. This file contains one JSON object per line.

Your task is to:
1. Analyze (reverse engineer / extract information from) the `/home/user/implant` binary to identify the Command & Control (C2) domain used by the attacker. You know from previous threat intel that the attacker's domains always end with the `.xyz` Top-Level Domain.
2. Parse the `/home/user/csp_violations.jsonl` log file to find all CSP violation reports where the `csp-report.blocked-uri` field contains or matches the exact C2 domain you extracted from the binary.
3. For all matching log entries, extract the `source_ip` field (which is at the root of the JSON object, alongside the `csp-report` object).
4. Save the unique, alphabetically sorted IP addresses of these compromised hosts to `/home/user/compromised_ips.txt`, with one IP address per line.

Use Bash commands, `jq`, `strings`, or other shell utilities as needed. Ensure your final output file contains only the list of IP addresses.