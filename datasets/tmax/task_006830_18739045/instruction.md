You are a security engineer tasked with rotating credentials for a legacy data processing service. As part of the migration, you need to recover the old credential, generate a new encoded token for the updated authentication flow, and prepare a strict firewall configuration to isolate the legacy service during the transition.

Perform the following tasks on the system:

1. **Credential Recovery (Brute-force):**
   The file `/home/user/legacy_hash.txt` contains the SHA-256 hash of the legacy system's password.
   You know from old documentation that the password is exactly 6 characters long, begins with the prefix `sec`, and the remaining 3 characters are exclusively lowercase alphabetic letters (`a-z`) or digits (`0-9`).
   Write a Rust program in the directory `/home/user/cracker` to brute-force this hash and recover the original plaintext password. 

2. **Payload Encoding:**
   Once you have recovered the password, you must create a new authentication token for the updated service. The new token must be the standard Base64 encoding of the following string:
   `<recovered_password>:NEW_AUTH_FLOW`
   (Substitute `<recovered_password>` with the actual 6-character password you found).
   Save this exact Base64 encoded string to the file `/home/user/new_token.txt`. There should be no trailing newlines in the file.

3. **Firewall Policy Configuration:**
   To secure the legacy service (running on port 9999) during rotation, you need to prepare an `iptables` IPv4 ruleset. You do not have root access to apply it, so you must generate the configuration file that will be loaded later via `iptables-restore`.
   Create a file at `/home/user/firewall.rules` with the following strict specifications:
   - The default policy for the `INPUT` chain must be `DROP`.
   - The default policy for the `FORWARD` chain must be `DROP`.
   - The default policy for the `OUTPUT` chain must be `ACCEPT`.
   - Add exactly one rule: Accept incoming TCP traffic on destination port `9999` exclusively from the source IP address `10.0.0.45`.
   The file must be in valid `iptables-save` format (including the `*filter` table declaration and the `COMMIT` keyword).

All work must be done within the `/home/user` directory. You may use standard CLI tools and Rust (Cargo is available).