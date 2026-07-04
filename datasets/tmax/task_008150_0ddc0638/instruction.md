You are a security researcher analyzing a suspicious Python-based exfiltration tool that crashed on a compromised Linux host. You have been provided with an investigation directory containing the artifacts left behind. 

Your objective is to recover the exfiltrated data by analyzing the network traffic, the stack trace, and a raw memory dump. Write a Python script to automate this analysis and extract the final flag.

The artifacts are located in `/home/user/investigation/`:
1. `crash_report.txt`: A detailed Python stack trace generated when the malware crashed. The malware was using a deleted configuration file.
2. `memory.dump`: A raw binary memory dump of the crashed process. The malware's configuration file was deleted from disk, but its contents (which include part of the encryption key) are still present in this memory dump.
3. `capture.pcap`: A network packet capture of the malware's exfiltration traffic.

Perform the following steps:
1. **Stack Trace Analysis**: Inspect `crash_report.txt`. The traceback contains local variables at the time of the crash. Identify the value of the `partial_key` string variable.
2. **Deleted File / Core Dump Recovery**: Scan `memory.dump` using Python to carve out the remaining part of the key. The missing key fragment is enclosed between the exact byte signatures `KEY_START_` and `_KEY_END`. Extract this fragment.
3. **Key Reconstruction**: The complete encryption key is the concatenation of `partial_key` and the extracted fragment from the memory dump (e.g., if partial_key is `ABC` and the fragment is `DEF`, the full key is `ABCDEF`).
4. **Pcap Analysis and Corrupted Input Handling**: Write a Python script (you may use the `scapy` library) to read `/home/user/investigation/capture.pcap`. 
   - The pcap contains UDP traffic sent to port `1337`.
   - The malware's author was sloppy, and the pcap contains corrupted packets that may cause standard parsing functions to throw exceptions. You must handle these exceptions gracefully and extract the raw data payloads of all *valid* UDP packets sent to port `1337`.
   - Concatenate the extracted payloads in the order they appear.
5. **Decryption**: The concatenated payload is XOR-encrypted. Decrypt it using the full reconstructed key. The XOR key should be repeated to match the length of the concatenated payload.

Write the final decrypted string to `/home/user/investigation/decrypted_flag.txt`. Do not include any trailing newlines unless they are part of the decrypted payload.