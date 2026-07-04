You are a network engineer analyzing suspicious traffic captured from a potentially compromised workstation. You have extracted a hexadecimal payload from a packet capture, as well as the source code of the custom encryption tool the rogue insider used to exfiltrate data. 

In your workspace, you will find the following files:
1. `/home/user/custom_crypto.py` - The flawed Python script used by the insider to encrypt their files.
2. `/home/user/captured_traffic.hex` - A continuous hex string representing the encrypted payload exfiltrated over the network.

Intelligence suggests that the exfiltrated file is a standard PNG image. 

Your objectives are to:
1. Analyze the `custom_crypto.py` script to identify the specific Common Weakness Enumeration (CWE) identifier that best describes the fundamental cryptographic flaw (Use of a Broken or Risky Cryptographic Algorithm / Weak PRNG / etc.).
2. Perform a known-plaintext cryptanalysis attack to recover the encryption key. (Hint: Think about standard file headers).
3. Write a Python script to decrypt the payload in `/home/user/captured_traffic.hex` back into its original binary form.
4. Save the decrypted binary file to `/home/user/decrypted_image.png`.
5. Verify the integrity of your decrypted file by calculating its SHA256 hash.

Finally, create a report file at `/home/user/report.txt` with exactly three lines in the following format:
Line 1: The exact CWE ID of the vulnerability (e.g., CWE-123)
Line 2: The recovered encryption key represented as a lowercase hex string (e.g., aabbccdd)
Line 3: The SHA256 hash of `/home/user/decrypted_image.png`

Do not include any extra text, spaces, or formatting in `report.txt` outside of these three lines.