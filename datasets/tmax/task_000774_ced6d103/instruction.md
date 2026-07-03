You are a red-team operator preparing for an engagement against a highly restricted environment. The target environment uses a proprietary, custom-built Intrusion Detection System (IDS) that scans all incoming files. 

We have managed to exfiltrate a stripped version of the target's IDS engine, located at `/app/target_ids`. 
However, the binary only runs on a specific legacy architecture emulator, making it extremely slow. To build and rapidly fuzz our evasion payloads offline, we need a lightweight, pure Python clone of this IDS's detection logic.

Your task is to create a Python script at `/home/user/offline_ids.py` that perfectly replicates the static analysis classification logic of `/app/target_ids`.

**Available Resources:**
1. The stripped binary: `/app/target_ids`
2. A training corpus of files we have already tested against the real IDS:
   - `/home/user/training_data/blocked/` (Files the IDS flagged as malicious)
   - `/home/user/training_data/allowed/` (Files the IDS allowed)

**Requirements for `/home/user/offline_ids.py`:**
- Must take exactly one command-line argument: the absolute path to a file to analyze.
- Must perform pattern matching, TLS certificate analysis, and ELF binary format analysis, just as the original binary does.
- Must print exactly `BLOCKED` to standard output if the file matches the target's threat signatures.
- Must print exactly `ALLOWED` to standard output if the file is benign.
- Must run cleanly using the standard Python 3 libraries available on the system.

**Workflow:**
1. Reverse engineer the behavior of `/app/target_ids` using the provided training data and standard Linux analysis tools (e.g., `strings`, `objdump`, `readelf`, `hexdump`).
2. Identify the specific indicators of compromise (IoCs) across different file types (ELF headers/sections, XSS/Injection patterns in text, and suspicious TLS certificate fields).
3. Implement the exact equivalent logic in `/home/user/offline_ids.py`.

*Note: Your final script will be tested against a hidden evaluation corpus of both blocked and allowed files to ensure your logic is an exact match to the target IDS.*