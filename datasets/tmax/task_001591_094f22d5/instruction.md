You are a forensics analyst responding to a severe security breach on a Linux host. During your investigation, you recovered two key pieces of evidence left behind by the attacker:

1. A stripped, obfuscated ELF binary located at `/app/auth_module`. The attacker used this to generate authentication tokens to bypass the system's access controls.
2. An intercepted audio file located at `/app/voicemail.wav`. We believe this is a voicemail from one attacker to another, discussing a secret "salt" or key phrase injected into their token generation algorithm.

Your objective is to reverse-engineer the token generation algorithm used by the attacker and create a clean, standalone Bash script that replicates its functionality exactly. This script will be used by our threat intelligence team to predict attacker tokens and hunt for further compromises.

Requirements:
- Analyze the `/app/auth_module` ELF binary to understand the cryptographic operations (e.g., hashing, string manipulation) it performs on the input.
- Transcribe or listen to `/app/voicemail.wav` to recover the secret salt/phrase mentioned by the attacker.
- Write a Bash script at `/home/user/token_gen.sh`.
- The script must be executable (`chmod +x /home/user/token_gen.sh`).
- The script must accept exactly one argument (the input string).
- The script must output ONLY the final generated token to standard output, matching the exact behavior of `/app/auth_module` for any given alphanumeric string.

Ensure your Bash script is bit-exact equivalent to the oracle binary. Automated verifiers will fuzz both your script and the original binary with thousands of random inputs and assert that the outputs are completely identical.