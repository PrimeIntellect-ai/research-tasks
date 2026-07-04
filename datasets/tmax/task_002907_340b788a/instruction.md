You are a storage administrator dealing with massive amounts of system logs and audio voicemail recordings. Your system's disk space is critically low, and standard tools like `tar` and `zip` are not optimizing the audio files enough before packaging them. 

You need to write a custom archival tool in pure Bash that intelligently compresses different file types and packages them into a single, custom binary archive format.

Create an executable Bash script at `/home/user/archiver.sh` that takes exactly two arguments:
1. `input_dir`: The directory containing the files to archive.
2. `output_file`: The path to the resulting custom archive file.

### Archival Rules & Constraints
Your script must iterate through all files in the given `input_dir` (you do not need to handle nested subdirectories) and process them as follows:
- **Text Files (`*.log`, `*.txt`)**: Compress the raw file data using `gzip -9`.
- **Audio Files (`*.wav`)**: Use `ffmpeg` to convert the file to a highly compressed MP3 format before archiving. To save maximum space while preserving spoken word intelligibility, force the output to **mono channel** and a **32k audio bitrate**.

### Custom Archive Format Specification
The output file MUST strictly follow this exact binary layout:

**1. Manifest Section**
The file must start with the string `MANIFEST\n`.
Following that, list each processed file on a new line in the format:
`<filename> <size_of_compressed_binary_data_in_bytes>\n`
*(Note: Use just the base filename, not the full path).*

**2. Separator**
After the last manifest entry, add a line containing exactly:
`---DATA---\n`

**3. Binary Payload**
Immediately following the `\n` of the separator, append the raw compressed binary data for each file in the exact same order they were listed in the manifest. Do not add any newlines or padding between the binary chunks.

### Setup and Testing
To test your script, an environment has been prepared for you.
1. Create a directory `/home/user/data`.
2. Copy the system's raw audio recording from `/app/recording.wav` into `/home/user/data/voicemail.wav`.
3. Create a large dummy text log: `base64 /dev/urandom | head -c 5000000 > /home/user/data/system.log`
4. Run your script: `/home/user/archiver.sh /home/user/data /home/user/output.arc`

Your success will be measured by a strict **metric threshold**: the final `/home/user/output.arc` must be a valid custom archive (parseable by our automated systems) and its total file size must be less than **250,000 bytes** (representing a massive compression ratio from the original ~5MB + WAV size).