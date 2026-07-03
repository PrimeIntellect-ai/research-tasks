You are an operations engineer triaging an incident where a faulty backup shell script (which broke on filenames with spaces) corrupted a critical database journal file. 

You have been given access to the repository located at `/home/user/db_triage`, which contains the C source code for the database journal parser and the corrupted journal file itself.

Your objectives are:
1. **Secret Recovery:** The journal records are encrypted (XOR cipher). The 16-character recovery key was accidentally committed to the Git repository in the past and later removed. Find this key in the Git history.
2. **Corrupted Input Handling:** The C program `db_parser.c` is currently brittle. It reads sequential records but aborts immediately if it encounters corrupted data. You must modify `db_parser.c` so that if a record is invalid (e.g., checksum mismatch or impossible length), the program scans forward byte-by-byte to find the next valid record magic number (`0xCAFEBABE`) and recovers as many records as possible.
3. **Data Recovery:** Compile your fixed `db_parser.c`. Run it on the corrupted journal file (`corrupted journal with spaces.bin`) using the recovered XOR key.
4. **Output:** The decrypted payload of each valid record is a plain string in the format `KEY=VALUE`. Write all recovered strings to `/home/user/recovered_data.txt`, one per line, in the order they appear in the journal.

**Journal Record Format (Little Endian):**
- **Magic:** 4 bytes (`0xCAFEBABE`)
- **Payload Length:** 4 bytes (uint32)
- **Encrypted Payload:** `N` bytes (where `N` is Payload Length). Decrypt by XORing each byte with the 16-character recovery key (repeating cyclically).
- **Checksum:** 1 byte. This is the sum of all *decrypted* payload bytes modulo 256.

A record is only valid if the magic is correct, the length is reasonable (e.g., `< 1024`), and the checksum matches. If a record is invalid, your parser must recover by scanning for the next `0xCAFEBABE` magic.

Ensure the final extracted valid records are written exactly to `/home/user/recovered_data.txt`.