You are a compliance analyst generating audit trails for a legacy system. We have intercepted a batch of payloads, some of which are known to be clean, and some of which contain malicious intrusion attempts (SQL injection, XSS, or shellcode). 

Unfortunately, the payloads are encoded. The system uses a legacy, stripped compiled binary located at `/app/legacy_decoder` to decode them. The binary expects exactly two arguments: a 5-character lowercase alphabetical password, and the path to an encoded file. It outputs the decoded content to standard output. (e.g., `/app/legacy_decoder <password> <file>`).

We have provided two directories containing encoded payloads:
- `/app/corpus/clean/` (contains 50 encoded clean payloads)
- `/app/corpus/evil/` (contains 50 encoded malicious payloads)

Your task is to:
1. Discover the 5-character password. (Hint: All decoded clean payloads are known to start with the string "AUDIT_ENTRY:").
2. Analyze the decoded outputs of both corpora to identify the patterns or signatures that distinguish the `evil` payloads from the `clean` ones.
3. Write a C program at `/home/user/audit_filter.c` that acts as an intrusion detection classifier. 
4. Your C program must compile to `/home/user/audit_filter` (using `gcc /home/user/audit_filter.c -o /home/user/audit_filter`).
5. `/home/user/audit_filter` must take exactly one argument: the path to an *encoded* payload file. 
6. The compiled program must read the encoded file, decode it (you may invoke `/app/legacy_decoder` via `popen` or `system`, or reimplement its logic in your C code), and then scan the decoded payload for the malicious signatures you identified.
7. The program must terminate with **exit code 0** if the payload is clean, and **exit code 1** if the payload is malicious (evil).

Finally, generate an audit log at `/home/user/audit_trail.log` that lists the evaluation of all 100 payloads. Each line must be formatted exactly as:
`[CLEAN] /app/corpus/clean/payload_01.enc`
or 
`[EVIL] /app/corpus/evil/payload_01.enc`

Ensure your C code is robust and handles file I/O properly. The verification suite will test your `/home/user/audit_filter` binary against an unseen, hold-out corpus of payloads encoded with the same password and mechanisms.