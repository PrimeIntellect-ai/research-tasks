You are acting as a storage administrator managing disk space for a large-scale voice recording archival system. We are running out of space because our storage cluster is filled with undocumented backup files, many of which are corrupted, incorrectly formatted, or deliberately malformed files masquerading as `.wav` audio. 

Your objective is to write a Python script `/home/user/backup_compressor.py` that recursively traverses a target directory, filters out the corrupted or malicious files, and packs the valid files into a custom incremental backup format.

We have provided a reference audio file at `/app/reference_sample.wav`. Inspect this file to determine the standard audio format we use (specifically, you must extract its sample rate, number of channels, and bit depth). A "valid" backup file must strictly match these exact WAV format parameters. Any file that is malformed, lacks a valid RIFF/WAVE header, or deviates from the reference file's parameters (e.g., different sample rate, different channels, corrupted data chunks) must be rejected to save space and prevent downstream processing errors.

You will test your script against a corpus located at `/app/corpus/`. The corpus contains two subdirectories, though your script should handle the top-level directory recursively:
- `/app/corpus/clean/` contains valid audio files.
- `/app/corpus/evil/` contains malformed, corrupted, or fake WAV files.

Your Python script must take two positional arguments:
1. The input directory to traverse.
2. The output path for the custom backup archive.

Example invocation:
`python3 /home/user/backup_compressor.py /app/corpus /home/user/archive.mybak`

**Custom Compression Backup Format Requirements:**
Instead of a standard ZIP or tar, we use a custom concatenated binary format to track increments. The file `/home/user/archive.mybak` must be generated with the following exact structure:
- **Global Header**: The literal string `MYBAK_v1` (8 bytes).
- **File Entries** (for each valid file, appended sequentially):
  - File path length (2 bytes, unsigned short, little-endian)
  - Relative file path from the scanned root (e.g., `clean/audio1.wav`) as UTF-8
  - File size in bytes (4 bytes, unsigned int, little-endian)
  - Zlib compressed file content (using standard `zlib.compress`)

**Validation Logging:**
Your script must also generate a text log at `/home/user/filter.log`. Each line must contain exactly the relative file path and either `ACCEPTED` or `REJECTED`, separated by a comma. For example:
`clean/audio1.wav,ACCEPTED`
`evil/fake_audio.wav,REJECTED`

Ensure your script processes the corpus correctly, preserving 100% of the clean files and rejecting 100% of the evil files.