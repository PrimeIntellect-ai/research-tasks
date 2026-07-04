You are a security auditor tasked with analyzing a proprietary authentication service. During an engagement, you discovered a stripped binary at `/app/auth_cli` which is used to generate and validate permission tokens.

Our initial service auditing indicates that this binary implements a custom, non-standard checksum/hashing algorithm to sign permission strings before packaging them into tokens. To craft our own exploit payloads and test for privilege escalation vulnerabilities, we need a native Python implementation of this hashing algorithm.

Your task is to:
1. Reverse engineer the stripped binary `/app/auth_cli` to understand the internal hashing mechanism. 
2. Write a Python script at `/home/user/hash_algo.py` that replicates this logic perfectly.
3. The script must accept a single string as its first command-line argument (e.g., `python3 /home/user/hash_algo.py "admin:true"`) and print ONLY the resulting 8-character lowercase hex string to standard output.

Your implementation will be subjected to a rigorous automated test suite that compares its output to the original `/app/auth_cli` binary across a large set of randomly generated fuzzing inputs. You must achieve a 100% match rate to pass.