You are a penetration tester performing a security assessment on a legacy data processing service. You have intercepted a set of encrypted API payloads in the `/home/user/captures/` directory. 

Through earlier reconnaissance, you discovered the service uses a highly vulnerable custom stream cipher. The cipher simply XORs the plaintext with a repeating 4-byte static key. 

You also know the exact plaintext of one of the captured payloads. The file `/home/user/captures/admin_login.bin` is the encrypted version of the following exact 38-byte JSON string:
`{"user":"admin","role":"administrator"}`

Your objective is to exploit this cryptographic weakness, scan the remaining captures, and craft a new malicious payload. 

Please write and execute a Go program (or multiple Go programs) to accomplish the following tasks:

1. **Cryptanalysis (Key Recovery):** Perform a known-plaintext attack using `admin_login.bin` and the known JSON string to recover the 4-byte XOR key.
2. **Automated Scanning:** Using the recovered key, programmatically decrypt all `.bin` files in `/home/user/captures/`. Identify the file that contains the role `"system_backup"` in its decrypted JSON. Write the base filename (e.g., `file.bin`) of this capture to `/home/user/found_backup.txt`.
3. **Exploit Crafting:** Craft a malicious payload by encrypting the following exact JSON string using the recovered 4-byte key:
`{"user":"attacker","role":"system_root"}`
Save this newly encrypted binary payload to `/home/user/exploit.bin`.

Constraints:
* The Go code should be written to a file, compiled, and executed to perform the operations.
* All resulting files (`/home/user/found_backup.txt` and `/home/user/exploit.bin`) must have standard permissions and be readable.