You are acting as a technical writer organizing and updating documentation. You have received a batch of documentation updates from the engineering team in a custom binary packaging format, and you need to process these, convert their formatting, and create an incremental backup.

Here is your objective:

1. **Parse Custom Archives:** In the directory `/home/user/incoming/`, there are several files with the `.docpack` extension. These are custom binary files containing documentation. Each `.docpack` file has the following binary structure:
   - Bytes 0-3: The magic number `DOCP` (ASCII).
   - Bytes 4-7: The size of the payload text in bytes (32-bit integer, little-endian).
   - Bytes 8-39: The intended output filename (e.g., `intro.md`), padded with null bytes (`\x00`).
   - Bytes 40+: The raw text content of the documentation.

2. **Extract, Edit, and Convert:** Write a Python script to parse these files and extract the text. Before saving the text, apply the following macro-edits:
   - Replace all instances of the deprecated term `ProjectAlpha` with the new term `NexusOS`.
   - Convert custom header tags to standard Markdown. Specifically, convert `<<header1>>Any Text<</header1>>` to `# Any Text`.
   Save the processed `.md` files into the directory `/home/user/processed/` (create this directory if it doesn't exist).

3. **Incremental Backup:** There is an existing base backup archive located at `/home/user/base_docs.tar.gz`. It contains previous versions of the Markdown files.
   Compare your newly processed files in `/home/user/processed/` against the files inside `/home/user/base_docs.tar.gz`.
   Create a new archive at `/home/user/incremental_docs.tar.gz` that contains *only* the newly processed files that either:
   - Do not exist in the base archive.
   - Have different file content compared to their corresponding files in the base archive.
   *(Note: The files inside `incremental_docs.tar.gz` should not include the `processed/` directory structure; they should be at the root of the archive).*

4. **Logging:** Using standard stream redirection in your shell commands, pipe or redirect the list of filenames (just the basenames, e.g., `setup.md`) that were added to `incremental_docs.tar.gz` into a log file at `/home/user/changelog.txt`. Each filename should be on a new line. Sort the filenames alphabetically.

Ensure all final files (`/home/user/incremental_docs.tar.gz` and `/home/user/changelog.txt`) are created exactly at the specified paths.