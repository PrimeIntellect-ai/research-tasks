You are a forensics analyst investigating a compromised Linux workstation. The attacker has left behind persistent backdoors and a fragmented, encrypted archive containing exfiltrated data. Your job is to audit the system, remove the persistence mechanisms, and recover the stolen evidence.

Perform the following tasks using Bash and built-in Linux utilities. You must save your findings in specific files so they can be verified.

**Phase 1: SSH Hardening & Key Auditing**
The attacker added a rogue SSH key to `/home/user/.ssh/authorized_keys`. 
1. Audit the file. A legitimate key *must* end with the comment `admin@corp.local`. 
2. Remove any key that does not have exactly this comment from `authorized_keys`.
3. Save the completely removed rogue key(s) (the entire line) into `/home/user/rogue_keys.txt`.

**Phase 2: Privilege Escalation Auditing**
The attacker dropped a hidden binary with the SUID bit set in the `/home/user/system_backup` directory to maintain privilege escalation capabilities.
1. Find all files in `/home/user/system_backup` (and its subdirectories) that have the SUID bit set (`u+s`).
2. Calculate the SHA256 hash of each SUID file you find.
3. Compare these hashes against the known-good hashes listed in `/home/user/known_hashes.txt`.
4. Identify the binary whose hash is *not* in the known-good list.
5. Write the absolute path of this rogue SUID binary to `/home/user/rogue_suid.txt` (one path per line).

**Phase 3: Evidence Recovery & Cryptography**
The attacker staged exfiltrated data in `/home/user/exfil_parts/`. They split an encrypted archive into multiple chunks.
1. Reassemble the chunks in alphabetical order into a single file named `/home/user/encrypted_evidence.bin`.
2. Calculate the SHA256 checksum of `encrypted_evidence.bin` and ensure it matches the hash provided in `/home/user/exfil_hash.txt`.
3. The attacker encrypted this file using AES-256-CBC with PBKDF2. Through prior intelligence, we know the decryption password is the **exact filename (basename)** of the rogue SUID binary you discovered in Phase 2.
4. Decrypt `encrypted_evidence.bin` into a tar archive.
5. Extract the contents of the decrypted tar archive into the directory `/home/user/recovered_data/`.

Once you have completed all phases, ensure that `/home/user/rogue_keys.txt`, `/home/user/rogue_suid.txt`, and the files in `/home/user/recovered_data/` exist and contain the correct information.