You are acting as a configuration manager for a Linux system. You have been provided with an update package and an accompanying audio recording. Your task is to safely process the update, track changes, and compress the audio artefact.

1. **Safe Archive Extraction (Zip Slip mitigation):**
   There is a zip archive at `/app/update.zip`. This archive may contain a path traversal vulnerability (Zip Slip), attempting to overwrite files outside the intended extraction directory. 
   Write and execute a Bash script that safely extracts the contents of `/app/update.zip` into `/home/user/update_extracted/`. You must filter out or sanitize any file paths within the archive that attempt to escape the target directory (e.g., paths containing `../` or absolute paths pointing outside `/home/user/update_extracted/`). Files with safe paths should be extracted normally.

2. **Configuration Parsing and Incremental Backup:**
   Inside the safely extracted archive, there will be a file named `settings.conf`. 
   Read this configuration file to find the value of the `TargetDirectory` key. 
   Perform an incremental backup of the directory specified by `TargetDirectory` and save it to `/home/user/incremental_backup.tar.gz`. A previous full backup snapshot file (for `tar`'s listed-incremental feature) is available at `/app/backup.snar`. You must update this snapshot file and use standard stream redirection to output the list of backed-up files to `/home/user/backup_files.log`.

3. **Audio Compression:**
   There is an uncompressed audio artefact located at `/app/voice_memo.wav`. 
   To save space in our tracking system, compress this audio file into the Ogg Vorbis format and save it to `/home/user/compressed_memo.ogg`. You must heavily compress the file (e.g., by lowering the bitrate and sample rate) so that the resulting file size is minimized, but it must still be a valid decodable Ogg Vorbis file.

Ensure all outputs are placed exactly at the specified paths. You may use standard tools like `unzip`, `tar`, `awk`, `grep`, and `ffmpeg` which are available on the system.