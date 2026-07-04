You are tasked with recovering and organizing a developer's corrupted backup directory. The developer tried to create a backup script, but a bug caused it to follow symlinks recursively, creating infinite loops and duplicating compressed data archives. 

To make matters worse, the developer left the exact filtering requirements for the recovery in a voice memo, which you must first transcribe.

Your objectives are:

1. **Transcribe the Voice Memo**: 
   Analyze the audio file located at `/app/backup_recovery/voicenote.wav`. You may use Python's `SpeechRecognition` library or any available CLI tools (like `ffmpeg` combined with local STT if you install one) to understand the filtering parameters. The audio will specify:
   - A target **GCode Tool Number** (e.g., T0, T1, T2).
   - A target **ELF Architecture** (e.g., x86_64, ARM).
   - A target minimum **WAL Transaction ID**.

2. **Traverse and Parse**:
   Write a Python script to navigate `/app/backup_recovery/tangled_fs/`.
   - You must gracefully handle infinite symlink loops (never process the same physical file or directory twice).
   - Process files on-the-fly from inside compressed streams (`.gz` and `.zip`) without extracting them fully to disk.
   
3. **Format-Specific Extraction**:
   - **GCode** (`*.gcode.gz`): Sum the total extrusion distance (all `E` values on `G1` lines) *only* when the active tool matches the one from the voice memo.
   - **ELF** (`*.elf.zip`): Check the ELF header to determine if the machine architecture matches the one from the voice memo. (Store a boolean `true` if it matches).
   - **WAL** (`*.wal` within any archive): Parse the custom Write-Ahead Log binary format. (Format: 4-byte magic number `0x57414C00`, followed by sequential records. Each record is a 4-byte integer Transaction ID (Little Endian), followed by a 2-byte payload length, followed by the payload). Count how many records have a Transaction ID strictly greater than the number from the voice memo.

4. **Output Generation**:
   Create a single JSON file at `/home/user/extracted_metadata.json`. The keys should be the canonical absolute paths of the unique files you processed, and the values should be the extracted integer/boolean based on the logic above. Files that don't meet any matching criteria (e.g., ELF files of the wrong architecture) should still be included in the JSON with a value of `false` (for ELF) or `0` (for counts/sums).

Your final output will be evaluated automatically by an F1-score metric comparing your JSON to the hidden ground truth.