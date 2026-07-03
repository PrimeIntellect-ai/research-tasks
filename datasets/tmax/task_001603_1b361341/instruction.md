You are a backup administrator tasked with archiving and restoring legacy data from untrusted sources. 

You have received an old backup archive at `/home/user/backup.tar`. You suspect this archive might have been tampered with and could contain malicious paths designed to overwrite system files (a "zip slip" attack). Furthermore, the safe files in the archive are text files stored in various legacy encodings with Windows line endings, and they contain obsolete server references.

Your objective is to safely extract and clean the data. Perform the following steps:

1. Write a Go program named `/home/user/processor.go` (and run it) that reads `/home/user/backup.tar` and securely extracts its contents into the directory `/home/user/restored/`. 
2. During extraction, your Go program must detect any file paths within the tar archive that attempt directory traversal (e.g., paths containing `../` or starting with `/`). **Do not extract these files.**
3. Your Go program must write the exact archive paths of any detected malicious/rejected files into `/home/user/rejected.log`, one path per line.
4. After extraction, use standard shell tools (or expand your Go program) to process all the extracted files in `/home/user/restored/` (and its subdirectories):
   - Convert all text files to standard UTF-8 encoding. (Note: The files may currently be in UTF-16LE or Windows-1252).
   - Convert all files to use standard Unix line endings (LF instead of CRLF).
   - Find and replace all occurrences of the string `SERVER_LEGACY` with `SERVER_MODERN` across all extracted files.

The final state must have:
- The safe files extracted in `/home/user/restored/` with their text transformed and encoded in UTF-8.
- The `/home/user/rejected.log` file containing the rejected paths.