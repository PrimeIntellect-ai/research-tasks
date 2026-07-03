You are an artifact manager for a proprietary hardware ecosystem. Your team maintains a repository of compiled firmware packages (`.fw` files). Recently, the automated pipeline has been failing because the legacy C-based validation tool, located at `/app/fw_inspector`, is crashing on malformed files and allowing files with malicious metadata to pass through.

Your task is to write a robust Python-based curator script to replace the legacy tool's filtering phase. 

Requirements:
1. Create a Python script at `/home/user/curator.py` that takes two positional arguments: an input directory containing `.fw` files, and an output directory.
    Usage: `python3 /home/user/curator.py <input_dir> <output_dir>`
2. Reverse engineer the `.fw` binary format. You can use the stripped binary `/app/fw_inspector` (which simply prints the metadata of valid `.fw` files) to figure out the header structure, metadata format, and payload separation.
3. Your script must process all `.fw` files in the input directory:
    * Parse the binary structure.
    * Read the embedded structured metadata.
    * Identify and REJECT "evil" or malformed files. A file is considered invalid/evil if:
        a) The binary structure is malformed (e.g., claimed metadata length exceeds the file bounds).
        b) The embedded structured metadata specifies a target filename containing path traversal characters (e.g., `../`).
    * ACCEPT clean files by copying them exactly as-is to the output directory.
4. For all accepted files, generate a `manifest.json` inside the output directory. This file must be written atomically to avoid race conditions. The manifest should be a dictionary mapping the output filename (e.g., `firmware_1.fw`) to its SHA256 checksum.

You have access to standard Linux reverse-engineering tools (like `strace`, `strings`, `hexdump`, `objdump`) to analyze `/app/fw_inspector` and sample files if you wish to create them.

Your solution will be tested against two hidden corpora: a clean corpus that must be entirely accepted, and an evil corpus that must be entirely rejected.