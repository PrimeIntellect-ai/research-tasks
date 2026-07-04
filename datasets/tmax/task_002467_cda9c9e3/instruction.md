You are a forensics analyst investigating a compromised Linux host. We have isolated a directory containing artifacts left behind by the threat actor at `/home/user/evidence/`.

Inside this directory, there are two files of interest:
1. `/home/user/evidence/dropper.elf` - A compiled Linux executable used to establish persistence.
2. `/home/user/evidence/id_rsa` - An encrypted SSH private key used by the attacker for lateral movement.

Intelligence suggests that the passphrase for the encrypted SSH key is hardcoded as a SHA-256 hash within the `.rodata` section of `dropper.elf`. Furthermore, we know the attacker's passphrase generation pattern: it is exactly a 4-digit number followed by the string `admin` (e.g., `0000admin`, `1234admin`, `9999admin`).

Your task is to:
1. Extract the 64-character SHA-256 hash from the `.rodata` section of `/home/user/evidence/dropper.elf`.
2. Write a Python script at `/home/user/crack.py` to brute-force the extracted hash based on the known passphrase pattern. 
3. Save the cracked plaintext passphrase to `/home/user/passphrase.txt`.
4. Use the recovered passphrase to decrypt the SSH private key, and save the fully decrypted (unencrypted) private key to `/home/user/decrypted_id_rsa`. 

Ensure `/home/user/decrypted_id_rsa` has the proper permissions for an SSH key (0600) and contains the unencrypted `BEGIN OPENSSH PRIVATE KEY` block.