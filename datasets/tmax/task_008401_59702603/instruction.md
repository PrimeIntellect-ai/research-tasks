I am a technical writer organizing a corrupted documentation backup. My previous backup script got stuck in an infinite loop because our directory structure has cyclic symlinks (e.g., `v1` links to `v2`, which links back to `v1`). 

I need you to write and execute a Go script to recover the specific documentation files we need.

Here is what you need to do:
1. Parse the log file at `/home/user/backup.log`. This file contains multi-line records formatted exactly like this:
   ```
   ===RECORD START===
   Target: <file path>
   Status: <IGNORE | DECOMPRESS>
   Author: <name>
   ===RECORD END===
   ```
2. Identify all records where the `Status` is `DECOMPRESS`. Extract the `Target` file paths from these records.
3. Because of the cyclic symlinks in the paths provided in the log, you must resolve each `Target` path to its absolute, canonical file path (resolving all symlinks and safely avoiding infinite loops) before attempting to read it.
4. The target files are compressed using our proprietary "TechDocZ" format. To decompress a TechDocZ file:
   - Read the entire file as a single string.
   - Base64-decode the string into bytes.
   - Subtract 1 from the value of every resulting byte (e.g., if the byte value is 66, change it to 65).
   - Convert the final byte array back to a string.
5. Write the fully decompressed text from all processed files into a single output file at `/home/user/restored_docs.txt`. If there are multiple files, separate their contents with a single newline (`\n`). Write them in the order they appear in the log file.

Please write a Go script at `/home/user/restore.go`, run it, and ensure `/home/user/restored_docs.txt` is created with the correctly decompressed contents.