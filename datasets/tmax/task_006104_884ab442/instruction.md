Hello, IT Support. We have an urgent escalation ticket regarding a potential breach of our internal reporting service. Security suspects that an attacker managed to find an old API token and used it to exfiltrate data. 

We have provided you with three pieces of evidence on your machine:
1. A packet capture file at `/home/user/capture.pcap` which recorded the breach. Security noted that the attacker's payload contained the plaintext string `"UNAUTHORIZED_ACCESS"`.
2. A local Git repository at `/home/user/service-config` which contains the history of the service's configuration files. We suspect a developer accidentally committed the API token here in the past before removing it.
3. The service access log at `/home/user/service.log`.

Your task is to investigate this breach and resolve the ticket by performing the following steps:
1. Analyze the packet capture (`/home/user/capture.pcap`) to identify the Source IP address of the attacker who sent the `"UNAUTHORIZED_ACCESS"` payload. (Assume standard IPv4 traffic).
2. Investigate the Git history in `/home/user/service-config` to recover the leaked API token. The token was assigned to the "api_token" field in a JSON configuration file before being removed in a later commit.
3. Cross-reference your findings with `/home/user/service.log` to find the exact timestamp when this specific attacker IP successfully authenticated using the leaked token.

Once you have gathered this information, create a file at `/home/user/ticket_resolution.txt` with exactly the following format (replace the bracketed placeholders with your findings):

```
Attacker IP: [IP_ADDRESS]
Leaked Token: [TOKEN_STRING]
Breach Timestamp: [YYYY-MM-DD HH:MM:SS]
```

Please ensure the format matches exactly. Good luck.