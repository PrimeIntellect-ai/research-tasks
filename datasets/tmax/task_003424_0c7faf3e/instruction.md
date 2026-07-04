You are an incident responder analyzing a compromised Linux server. The attacker left behind a compiled binary (`/app/bin/alert_processor`) that processes raw network traffic logs to detect other intruders and crack their authentication tokens.

Your task is to write a clean Python implementation that perfectly replicates the behavior of this binary for safe analysis. You must write your script to `/home/user/process_alert.py`.

The attacker's binary uses the following logic, which your Python script must exactly mirror:
1. It takes a single command-line argument: a hex-encoded string representing a captured network payload.
2. It decodes the hex string into raw bytes.
3. It performs pattern matching to find an Intrusion Detection System (IDS) marker. Specifically, it searches for the byte sequence `0x49 0x44 0x53` (the ASCII string "IDS").
4. If the marker is not found anywhere in the payload, or if there are fewer than 4 bytes remaining after the marker, the program must print `NO_ALERT` and exit.
5. If the marker is found, the next 2 bytes represent the target network port (16-bit unsigned integer, big-endian). The program must print `PORT:<port_number>` without a newline.
6. The next 2 bytes immediately following the port represent a 16-bit target hash (16-bit unsigned integer, big-endian).
7. The program must brute-force a 2-character uppercase ASCII password (from "AA" to "ZZ") to match this hash. The attacker's custom hashing algorithm for a 2-character string `c1`, `c2` is defined as: `hash = (ord(c1) * 256 + ord(c2)) ^ port_number`.
8. If a matching 2-character password is found, append ` - CRACKED:<password>` to the output and print a newline. If no match is found, append ` - UNCRACKED` and print a newline.
   
Example execution:
`python3 /home/user/process_alert.py 0011224944531F904141`
- `0x49 0x44 0x53` is found.
- Next 2 bytes `0x1F 0x90` -> Port 8080.
- Next 2 bytes `0x41 0x41` -> Target hash 16705.
- Output: `PORT:8080 - CRACKED:KI`

Furthermore, you are required to use the `construct` library to parse the extracted 4-byte header (port and hash). The attacker left a vendored version of `construct-2.10.68` at `/app/construct-2.10.68/`. However, they deliberately sabotaged it to hinder analysis. You must locate and fix the perturbation inside the vendored package (hint: look in the package's `__init__.py` for a deliberate exception) before running your script. Make sure `/app/construct-2.10.68` is added to your `PYTHONPATH`.

Ensure your python script correctly handles edge cases, such as multiple "IDS" markers (it should only process the first one found), and payloads that are exactly long enough.