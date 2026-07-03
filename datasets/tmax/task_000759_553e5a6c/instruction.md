You are tasked with helping a developer securely organize and process project files, which involve handling video assets and securely unpacking archived datasets. 

Your task consists of two parts:

### Part 1: Video Asset Processing
We have a project demonstration video located at `/app/project_demo.mp4`. 
1. Use `ffmpeg` to extract the frames of this video at exactly 1 frame per second.
2. Save the extracted frames into the directory `/home/user/frames/`.
3. Use shell commands to bulk rename these frames so they follow the exact naming convention `frame_0001.jpg`, `frame_0002.jpg`, etc., in sequential order of their appearance in the video.

### Part 2: Secure Archive Extractor (Rust)
The project receives archived data from external untrusted sources. You must write a Rust command-line utility that securely extracts `.tar` files, protecting against path traversal and other malicious archive attacks.

1. Create a Cargo project at `/home/user/safe_tar`.
2. Write a CLI tool that takes two arguments: `safe_tar <input.tar> <output_dir>`.
3. The tool must stream the contents of the given `.tar` file.
4. **Validation**: Before extracting a file, the tool must verify its path. It MUST reject the entire archive if any entry contains:
   - Absolute paths (e.g., `/etc/passwd`)
   - Path traversal components (e.g., `../` or `..`)
   - Symlinks or hardlinks of any kind
5. **Extraction**: If the archive is completely clean, extract the files to `<output_dir>`. 
   - You must use atomic writes: write each file to a temporary name (e.g., `.tmp`) first, and then atomically rename it to its final path.
6. **Output**: 
   - If the archive violates any safety rules, the tool must print exactly `REJECT` to stdout, leave the `<output_dir>` empty (or clean up any partial extractions), and exit with status code `1`.
   - If the archive is safe and successfully extracted, the tool must print exactly `ACCEPT` to stdout and exit with status code `0`.

To test your tool, we have provided two corpora of `.tar` files:
- `/app/corpus/evil/`: Contains archives designed to exploit file system vulnerabilities. Your tool MUST reject 100% of these.
- `/app/corpus/clean/`: Contains normal, safe project archives. Your tool MUST accept and extract 100% of these.

Ensure your Rust tool compiles successfully (`cargo build --release`). The verification script will invoke your compiled binary directly against the corpora.