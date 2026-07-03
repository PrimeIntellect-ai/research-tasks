You are acting as a technical assistant for a technical writer who is organizing a chaotic legacy documentation repository. The writer needs to consolidate a large number of text files into a single, standardized, and cleanly formatted archive. 

However, the legacy repository (`/home/user/legacy_docs`) is notoriously messy. It contains infinite symlink loops created by past broken backup scripts, and the text files are saved in a mix of different character encodings (UTF-8, UTF-16LE, and ISO-8859-1). Additionally, the company recently rebranded from "AcmeCorp" to "ZenithInc", and all documentation needs to be updated during this consolidation.

Your task is to write and execute a Bash script (`/home/user/consolidate_docs.sh`) that does the following:

1. **Traverse the Directory Safely**: Recursively find all `.txt` files in `/home/user/legacy_docs`. You must include standard files and symlinks that resolve to standard files. You must explicitly avoid falling into infinite directory symlink loops.
2. **Standardize Encoding**: For each discovered `.txt` file, detect its character encoding and convert its contents to standard UTF-8.
3. **Macro Text Editing**: Replace all occurrences of the exact string `AcmeCorp` with `ZenithInc` in the text stream.
4. **Format and Combine**: Combine the processed text of all files into a single stream. Before the content of each file, prepend a header line exactly in this format: 
   `===<ABSOLUTE_PATH_OF_FILE>===`
   (e.g., `===/home/user/legacy_docs/chapter1/intro.txt===`). If the file is a symlink, use the path of the symlink itself, not the resolved target.
5. **Custom Compression**: Compress the final combined stream using `gzip`, and then encode the gzipped binary output using `base64`. 
6. **Output**: Save the final base64-encoded string to a single file at `/home/user/consolidated.b64gz`.

Ensure your script is robust. You may install standard utility packages (like `file`, `iconv`, etc.) if needed via `sudo apt-get` (assume passwordless sudo is available for standard package installation if required, but do not rely on root for the script execution itself). 

When you have finished creating the `/home/user/consolidated.b64gz` file, exit.