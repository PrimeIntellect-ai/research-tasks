You are a storage administrator managing a massive disk partition for a corporate telephony system. The system receives thousands of audio voicemail logs daily. Recently, a wave of audio spam and corrupted files has been exhausting disk space. 

You recently received a high-priority system voicemail located at `/app/voicemail_99.wav`. This audio file contains a spoken message from the security team detailing the exact keywords used in the recent voicemail spam campaign.

Your objective is to build a robust shell script to clean up the voicemail directories.

1. Transcribe `/app/voicemail_99.wav` (using available tools like `whisper` or `ffmpeg` pipelines) to discover the three secret spam keywords.
2. Create a bash script at `/home/user/cleanup.sh` that takes two arguments: a target directory containing `.wav` files, and the path to a manifest file.
    `bash /home/user/cleanup.sh <target_directory> <manifest_file>`
3. The script must iterate through all `.wav` files in the `<target_directory>` and perform the following:
    - **Validation**: Check if the file is a valid audio file (e.g., using `ffprobe`). If it is corrupted or not a true audio file, it must be deleted.
    - **Transcription**: Transcribe the valid audio files.
    - **Filtering**: If the transcript contains ANY of the three secret spam keywords identified in `voicemail_99.wav` (case-insensitive), the file must be deleted.
    - **Preservation & Manifest**: If the file is valid and clean (contains no spam keywords), it must be preserved. The script must compute its SHA256 checksum and append it to the `<manifest_file>` in the format `<checksum>  <filepath>`.
    - **Concurrency**: Because the telephony system might invoke your script concurrently on different subdirectories, your script MUST use file locking (e.g., `flock`) when writing to the `<manifest_file>` to prevent race conditions and interleaved writes. You should also ensure temporary files created during transcription are managed securely and deleted via `trap` on exit.

Write the script using standard bash built-ins, coreutils, `ffprobe`, and the available transcription tools. Test your script to ensure it accurately filters files and safely writes the checksum manifest.