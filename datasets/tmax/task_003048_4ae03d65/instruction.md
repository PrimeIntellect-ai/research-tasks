You are a DevSecOps engineer tasked with modernizing our infrastructure's policy-as-code enforcement. 

We have a legacy, compiled C binary located at `/app/policy_engine.bin` that evaluates network connections and SSH key configurations to generate a strict risk score and policy enforcement token. This tool is currently used in our deployment pipeline to authorize or reject service configurations based on our internal network and SSH hardening guidelines.

We need to deprecate this black-box binary. Your task is to reverse-engineer its behavior and rewrite it entirely in Python.

1. Analyze `/app/policy_engine.bin`. You can pass it test inputs via standard input (`stdin`). 
   The expected input format is a single line containing space-separated values:
   `<IP_ADDRESS> <PORT> <SSH_KEY_TYPE> <KEY_LENGTH>`
   (Example: `192.168.1.50 22 rsa 2048`)

2. Write a Python script at `/home/user/policy_engine.py` that exactly replicates the binary's behavior. 
   - It must read a single line from `stdin` in the exact same format.
   - It must output the exact same formatted string to `stdout` as the legacy binary, including any calculated risk scores, policy actions, and cryptographic hashes.
   - Any secret salts or static rules hardcoded in the legacy binary must be accurately extracted and implemented in your Python script.

Your final deliverable must be the Python script at `/home/user/policy_engine.py`. An automated system will fuzz your script with thousands of randomly generated audit logs and compare the output bit-for-bit against the legacy binary.