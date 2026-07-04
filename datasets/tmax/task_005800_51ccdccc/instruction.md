You are helping a technical writer organize a messy dump of documentation provided by different engineering teams. You have been given a master archive located at `/home/user/docs_archive.tar`. 

Inside this tar file, there are various nested archives and compressed files (`.zip`, `.tar.gz`, `.md.gz`). Some of the archives provided by the teams were corrupted during transfer.

Your task is to write and execute a Python script that does the following:
1. Opens `/home/user/docs_archive.tar` and processes its contents without extracting the master archive to disk (process streams in memory or extract nested items temporarily).
2. Verifies the integrity of each nested archive/compressed file. If an archive is corrupted or invalid, skip it entirely and print a warning.
3. Extracts the contents of all valid Markdown (`.md`) files found within the valid nested archives or compressed streams. 
4. Compiles all extracted Markdown content into a single consolidated file. For each Markdown file found, prepend its content with a level 1 Markdown header containing exactly its base filename (e.g., `# api.md`), followed by a newline, followed by the file's original text, followed by another newline.
5. Sort the sections alphabetically by the base filename of the Markdown files. If two files have the same name in different archives, sort them by their relative path inside the archives.
6. Write the final compiled text to `/home/user/compiled_docs.md`. **Crucially, you must use atomic writing**: write the compiled content to a temporary file first, then atomically move/rename it to `/home/user/compiled_docs.md` to prevent any data corruption in case the process is interrupted.

Do not install any external Python libraries; use Python's built-in standard library (`tarfile`, `zipfile`, `gzip`, `tempfile`, `shutil`, `os`, etc.). 

Run your script to produce `/home/user/compiled_docs.md`.