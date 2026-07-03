You are tasked with recovering an automated configuration dictation from a corrupted, chunked backup and implementing a tracking mechanism.

Our legacy configuration manager used to backup audio dictations of our firewall rules. The backup mechanism split the audio file into multiple chunks, stored them in nested zip archives, and distributed them across a directory structure. Recently, some files were corrupted. 

Your objectives are:

1. **Reconstruct the Audio Payload:**
   - Recursively traverse the directory `/app/legacy_backups/`.
   - Extract all `.zip` files you find (some may be nested).
   - Inside, you will find chunked binary files named `chunk_NNN.bin` and corresponding `chunk_NNN.md5` files.
   - Verify the integrity of each chunk using its MD5 hash. Discard any chunk that fails the integrity check.
   - Merge the remaining, valid chunks in sequential order to reconstruct the original audio file. Save this to `/home/user/recovered.wav`. (If a chunk is missing or corrupted, simply concatenate the subsequent valid chunk directly).

2. **Transcribe the Configuration:**
   - Use a speech-to-text library in Python (such as `openai-whisper`, which you can install via pip) to transcribe `/home/user/recovered.wav`.
   - Save the raw transcribed text to `/home/user/firewall_rules.txt`. Make sure the text is fully decoded.

3. **Implement a Configuration File Watcher:**
   - Write a Python script at `/home/user/watcher.py` that uses a library like `watchdog` to monitor the directory `/app/active_config/` for any file modifications.
   - When a file in that directory is modified, the script should automatically create a split zip archive (chunks of 500KB) of the entire directory and place the backup pieces in `/app/backup_staging/`. (You do not need to run the watcher as a daemon for the final submission, just write the complete, functional script).

Ensure that your transcription process yields the highest accuracy possible. Your final success will be evaluated by comparing the text in `/home/user/firewall_rules.txt` against the ground truth transcript using a string similarity metric (Levenshtein ratio).