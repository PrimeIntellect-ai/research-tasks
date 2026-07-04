You are a security researcher analyzing a suspicious binary. You have a local sandbox environment to intercept its Command and Control (C2) traffic, but the sandbox configuration is broken. Furthermore, a custom protocol parser used to analyze the malware's payloads keeps crashing, and you need to figure out why, fix it, and write a classifier to detect malicious payloads.

Your task has three phases:

**Phase 1: Fix the Sandbox Environment**
In `/home/user/sandbox/`, there is a startup script `start_sandbox.sh` that launches three services: `dnsmasq`, `nginx`, and a `flask` sinkhole server.
Currently, the end-to-end flow is broken. The malware attempts to connect to `http://c2-malware.local:8080/`.
1. Modify `/home/user/sandbox/dnsmasq.conf` so that `c2-malware.local` resolves to `127.0.0.1`.
2. Modify `/home/user/sandbox/nginx.conf` so that it listens on port `8080` and proxies requests to the Flask sinkhole running on `127.0.0.1:5000`.
When properly configured, running `curl http://c2-malware.local:8080/ping` should return `{"status": "sinkholed"}`.

**Phase 2: Analyze and Fix the Protocol Parser**
In `/home/user/evidence/`, you will find:
- `parser.c`: A custom tool designed to parse the malware's binary payload format.
- `capture.pcap`: A network capture containing a malicious payload that crashes the parser.
- `core.parser`: A core dump from the crashed parser.

Analyze the pcap and core dump to understand the crash. The parser has an off-by-one boundary condition and a loop termination failure when reading chunked data.
Fix `parser.c` so that it correctly parses malicious payloads without crashing or infinite looping. Compile your fixed version to `/home/user/evidence/parser_fixed`.

**Phase 3: Create a Payload Classifier**
Based on your analysis of the vulnerability triggered by the malicious payload in Phase 2, write a script at `/home/user/classifier.py`.
This script must act as a detector. It should take a single command-line argument (the path to a payload file) and determine if it is a benign heartbeat ("clean") or an exploit attempt ("evil").
- If the payload is malicious, print exactly `EVIL` to standard output.
- If the payload is benign, print exactly `CLEAN` to standard output.

Your classifier will be evaluated against two hidden directories containing hundreds of samples. It must achieve 100% accuracy.