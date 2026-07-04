You are tasked with creating a data extraction and normalization tool for our legacy backup system. As a backup administrator, I need a script that can process nested backup archives and synchronize their metadata with a video-based timestamping mechanism.

Please create an executable program at `/home/user/process_backup` (you may write it in any language, but standard Linux command-line tools are recommended and pre-installed).

The program must accept exactly two positional arguments:
1. The path to a nested backup archive (a `.tar.gz` file).
2. The path to a synchronization video (an `.mp4` file).

When executed, your program must perform the following workflow and print the final output exactly as specified to standard output (`stdout`):

**Step 1: Video Synchronization Analysis**
Analyze the provided `.mp4` video file (Argument 2). Calculate the exact total number of video frames it contains. Let this integer be `F`. (Note: use reliable frame counting methods, such as parsing `ffprobe` packet counts or `ffmpeg` streams).

**Step 2: Archive Extraction**
Extract the `.tar.gz` backup archive (Argument 1). Inside the root of this archive, you will always find exactly two files:
- `meta.json`
- `data.zip`

**Step 3: Configuration Parsing**
Read `meta.json`. It contains a flat JSON object. Extract the value of the key `"encoding"`. This value represents the original character encoding of the log files contained in the backup (e.g., `UTF-16LE`, `ISO-8859-1`, `CP1252`).

**Step 4: Data Decoding**
Extract `data.zip`. It contains an arbitrary number of text files with the `.log` extension. 
For each `.log` file:
- Read its contents using the character encoding specified in `meta.json`.
- Convert the contents to standard `UTF-8`.

**Step 5: Output Generation**
Concatenate the newly UTF-8 encoded contents of all `.log` files in strict alphabetical order of their filenames (e.g., `a.log` then `b.log`).
Finally, print to standard output (`stdout`):
- `F` copies of the character `#` (where `F` is the frame count from Step 1).
- A single newline character (`\n`).
- The concatenated UTF-8 log data (no extra newlines between files unless they were present in the source files).

**Testing:**
I have placed a sample synchronization video at `/app/system_status.mp4` and a sample archive at `/app/sample_backup.tar.gz` for you to test your program. Make sure `/home/user/process_backup` is marked as executable (`chmod +x`). Once you are confident your script perfectly matches the requirements, you may conclude the task. Our automated systems will run your script against several unseen archive/video pairs to verify its correctness.