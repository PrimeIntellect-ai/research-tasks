You are acting as a storage administrator for our company. We need to implement a new data archival filtering script to save disk space, but the senior admin left the exact archiving criteria in a voice memo before going on vacation.

Your tasks are to:
1. Locate the voice memo at `/app/voicemail.wav` and transcribe it (e.g., using `whisper-cli` or similar tools available in your environment). The memo contains the exact threshold size in MB and the specific file extensions that should be included in the new archival process.
2. Read the legacy configuration file at `/etc/archival/legacy_policies.conf`. Combine the metadata filters specified in this config with the rules from the voice memo.
3. Write a Bash script at `/home/user/archive_filter.sh` that takes a continuous stream of newline-separated file records from standard input.
   - Input format: `<file_path> <size_in_bytes> <last_modified_timestamp>`
   - Your script must filter these records based on the combined rules (from the voicemail and config).
   - For records that pass the filter, the script must output a transformed format to standard output: `ARCHIVE_REQ|base64_encoded_filepath|size_in_kb` (size rounded down to nearest KB).
   - Your script must use standard bash built-ins and coreutils. No Python or Perl.

Your script will be aggressively tested against our reference implementation with random input streams to ensure it perfectly matches the expected behavior. Ensure it handles edge cases in file paths (like spaces) correctly and processes streams efficiently. Make sure it is executable (`chmod +x /home/user/archive_filter.sh`).