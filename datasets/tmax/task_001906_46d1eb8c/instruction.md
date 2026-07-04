You are tasked with recovering the state of a configuration management system from a forensic video recording of its deployment logs. 

A screen recording of the configuration manager's console output was captured and saved to `/app/deploy_logs.mp4`. The video displays a scrolling multi-line log of system changes. Your goal is to extract these logs, parse them, and execute the filesystem changes they describe to reconstruct the configuration state.

Step 1: Frame Extraction & Parsing
- Install `tesseract-ocr` and any necessary dependencies.
- Use `ffmpeg` to extract frames from `/app/deploy_logs.mp4` and run OCR to extract the log text. 
- The log contains multi-line records in the following format:
  ```
  BEGIN_TX
  ACTION: <CREATE_FILE | CREATE_SYMLINK | CREATE_HARDLINK | COMPRESS_STREAM>
  PATH: <file path relative to /home/user/sys_root>
  [TARGET: <target path for links>]
  [DATA: <base64 encoded data for files>]
  END_TX
  ```

Step 2: State Reconstruction
- Write a Bash script `/home/user/reconstruct.sh` that processes the extracted text.
- Clean up the OCR output using `sed` or `awk` to fix common artifacts and concatenate multi-line log records properly.
- Execute the actions to reconstruct the directory tree under `/home/user/sys_root/`. 
- For `COMPRESS_STREAM` actions, take the file at `PATH`, compress it using `gzip`, save it as `PATH.gz`, and remove the original file.

Step 3: Manifest Generation
- After reconstruction, your script must generate a final manifest at `/home/user/manifest.txt`.
- The manifest should list all files and links in `/home/user/sys_root/` sorted alphabetically by path.
- Format: `<file_type_indicator> <relative_path> <sha256sum or link_target>`
  - File type indicator: `F` for regular file, `S` for symlink, `H` for hardlink.

Ensure your bash script is robust to missing or slightly mangled OCR text. You must execute `/home/user/reconstruct.sh` to produce the final `/home/user/manifest.txt`.