You are managing the configuration backups for a legacy system. The system outputs its configuration files in an old character encoding, and you need to process these files to store them efficiently in our modern backup system. 

Your task is to write a script or execute commands to process a set of legacy configuration files located in `/home/user/legacy_configs`.

Here are the requirements for the backup process:
1. **Find and Convert**: Read all `.ini` files in `/home/user/legacy_configs`. These files are currently encoded in `UTF-16LE`. Convert their contents to `UTF-8`.
2. **Merge**: Combine all the converted files into a single continuous UTF-8 string. The files must be processed in alphabetical order based on their filenames. 
   - Immediately before appending the contents of each file, you must insert a header line with the exact format: `---FILE:[filename]---\n` (e.g., `---FILE:app.ini---\n`). 
   - Do not add any extra newlines other than the one at the end of the header and the newlines already present in the source files.
3. **Chunk**: Split the resulting merged UTF-8 string into smaller files of exactly 50 bytes each (the final chunk may be smaller). 
   - Save these chunks in the directory `/home/user/backup/`.
   - Name the chunks sequentially using zero-padded two-digit numbers, starting from zero: `chunk_00`, `chunk_01`, `chunk_02`, etc.
4. **Manifest Generation**: Create a manifest file at `/home/user/backup/manifest.txt`. 
   - This file must contain one line per chunk in the format: `[chunk_filename] [sha256_hash]`.
   - Example line: `chunk_00 a1b2c3d4e5f6...`
   - The chunks in the manifest must be listed in sequential order.

Ensure all directories are created if they do not exist. You may use any programming language or standard command-line tools available on a standard Linux system to accomplish this.