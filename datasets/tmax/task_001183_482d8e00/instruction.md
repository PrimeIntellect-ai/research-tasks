You are tasked with building the core application logic for a custom configuration management system that replays changes from a proprietary Write-Ahead Log (WAL) to a directory of configuration files. 

Your first task is to recover the historical configuration state to use as a testbed. 
1. There is an audio file at `/app/passphrase.wav`. It contains a spoken English passphrase.
2. Use this passphrase to decrypt and extract the nested archive located at `/app/historical_state.zip` into `/home/user/test_state/`. (The archive contains a multi-part split zip, which you will need to reassemble and extract to see the sample configs and sample WAL).

Your primary task is to write a robust Python script at `/home/user/wal_applier.py` that can replay our custom WAL format against a target directory.
The script must have the following CLI signature:
`python3 /home/user/wal_applier.py <passphrase> <wal_file> <target_dir>`

Behavioral requirements for `wal_applier.py`:
1. **Passphrase Check**: The script must first check if the provided `<passphrase>` exactly matches the spoken passphrase from `/app/passphrase.wav` (all lowercase, no punctuation, spaces between words). If it does not match, the script MUST immediately exit with status code 42.
2. **WAL Execution**: The WAL file is a plain text file where each line is a command. Empty lines or lines starting with `#` should be ignored. The commands must be executed in order on the `<target_dir>`.
3. **Command: `RENAME_EXT <old_ext> <new_ext>`**
   Bulk renames all files in `<target_dir>` (non-recursive) ending with `.<old_ext>` to end with `.<new_ext>`.
4. **Command: `CHUNK_FILE <filename> <chunk_size_bytes>`**
   Finds `<filename>` in `<target_dir>`. If it exists, reads it as binary and splits it into files named `<filename>.part000`, `<filename>.part001`, etc., each exactly `<chunk_size_bytes>` long (the last chunk contains the remainder). The original `<filename>` must then be deleted.
5. **Command: `CONVERT_KV_JSON <filename>`**
   Reads `<filename>` (which contains `key=value` lines), converts it to a standard JSON object, and overwrites `<filename>` with the formatted JSON (using `json.dump` with `indent=2`). Ignore lines without `=`.

Write your program carefully. It will be rigorously tested against a secret, reference binary oracle using randomly generated directories and WAL files. Your script's resulting directory structure, file contents, and exit codes must be bit-for-bit identical to the oracle's output.