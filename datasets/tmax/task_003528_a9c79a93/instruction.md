You are an incident responder investigating a recent breach. We have recovered two files from a compromised server:
1. `/home/user/dropper.elf`: A suspicious Linux executable.
2. `/home/user/payload.zip`: An encrypted archive that we believe contains the next-stage malware configuration. We also have its expected SHA256 checksum in `/home/user/payload.sha256`.

Preliminary reverse engineering indicates that the `dropper.elf` file contains a custom ELF section named `.keydata`. This section holds a string in the format `KEY_PREFIX=<prefix_string>`.

The attackers used this prefix, appended with a 2-digit number (from `00` to `99`), as the password for the `payload.zip` archive. 

Your task is to:
1. Write a Go program at `/home/user/analyze.go` that parses `/home/user/dropper.elf` (using the standard `debug/elf` package) to extract the prefix from the `.keydata` section.
2. Use this prefix to brute-force the `payload.zip` archive (testing suffixes `00` through `99`). You may use a combination of Go and standard shell tools to achieve this.
3. Extract the contents (`payload.bin`) to `/home/user/payload.bin`.
4. Verify that the extracted `payload.bin` matches the SHA256 hash provided in `/home/user/payload.sha256`.
5. Write the successfully cracked password to `/home/user/password.txt` (the file should contain only the password string, with no newline or trailing spaces).

Everything you need is in `/home/user`. Ensure your final extracted file and password file are exactly where requested.