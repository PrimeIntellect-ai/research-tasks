You are a compliance analyst tasked with generating an audit trail from a legacy system's encrypted backups. You have been provided with a directory containing an encrypted archive, a file containing the expected file hashes, and a note about the password policy. 

Your objective is to decrypt the archive, extract its contents, verify the integrity of the extracted logs, and generate a compliance report.

Directory Location: `/home/user/audit_data/`

Inside this directory, you will find:
1. `audit_backup.enc`: A tarball (`.tar.gz`) encrypted using OpenSSL with the `aes-256-cbc` cipher and the `-pbkdf2` key derivation function.
2. `hashes.txt`: A file containing the expected SHA-256 hashes of the files inside the archive (in standard `sha256sum` output format).
3. `key_policy.txt`: A text file indicating the strict format of the backup passwords used during that era.

Task Steps:
1. Read the `key_policy.txt` to understand the password format.
2. Brute-force or programmatically find the correct password to decrypt `audit_backup.enc` into a standard `.tar.gz` file, and extract its contents into `/home/user/audit_data/`.
3. Verify the SHA-256 hashes of the extracted files against the expected hashes listed in `hashes.txt`. Note: Storage degradation may have caused some files in the archive to become corrupted, meaning their extracted hashes will not match the expected hashes in `hashes.txt`.
4. Create a final compliance report at `/home/user/compliance_report.txt`. This file must contain ONLY the filenames of the logs that successfully matched their expected SHA-256 hashes. List exactly one filename per line, sorted in alphabetical order. Do not include the directory path in the filenames.

You may use any scripting language (Bash, Python, etc.) available on the system to complete these tasks.