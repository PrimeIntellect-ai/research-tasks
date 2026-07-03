You are tasked with a large-scale configuration migration based on a voice memo left by the lead DevOps engineer.

1. **Listen to the Voice Memo:** 
   There is an audio file located at `/app/voice_memo.wav`. You need to transcribe this audio to determine the exact string replacement operation required for our legacy configuration files. The memo will specify an old configuration value and its new replacement.

2. **Process the Configuration Files:**
   A directory at `/home/user/legacy_configs` contains thousands of `.ini` configuration files nested within various subdirectories.
   Write a Python script that:
   - Recursively traverses `/home/user/legacy_configs` to find all `.ini` files.
   - Reads each file in chunks if necessary and applies the large-scale text replacement dictated by the voice memo.
   - Processes the files concurrently (e.g., using Python's `multiprocessing` or `concurrent.futures` module).

3. **Generate a Locked Manifest:**
   As your concurrent workers update the files, they must append an entry to a shared manifest file at `/home/user/update_manifest.csv`. 
   - Because multiple processes will write to this manifest simultaneously, you **must** use file locking (e.g., via the `fcntl` module) to prevent race conditions and interleaved lines.
   - The format for each line in the manifest must be: `relative/path/to/file.ini,<SHA256_HEX_CHECKSUM_OF_NEW_FILE>`
   - The paths should be relative to `/home/user/legacy_configs/`.

Make sure your Python script is efficient, robust, and correctly implements file locking when updating the shared manifest. The final verification will evaluate the correctness of the entries in `/home/user/update_manifest.csv`.