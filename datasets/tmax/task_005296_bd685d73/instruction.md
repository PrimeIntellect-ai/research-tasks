I am a technical writer organizing our documentation, and our doc generator just produced a massive multi-line error log because several markdown files are missing their JSON frontmatter. 

I need you to write a Go script at `/home/user/fix_docs.go` that automates fixing this. The script must process the log file by reading from **standard input (stdin)** (e.g., using `os.Stdin`).

The log file is located at `/home/user/docs_build.log` and contains multi-line error records in this exact format:
```
[ERROR] File: /home/user/docs/setup.md
[DETAILS] Missing metadata. Suggested JSON:
{
  "author": "jane.doe",
  "status": "draft"
}
[END]
```

Your Go script must:
1. Parse these multi-line log records from standard input.
2. Extract the file path and the suggested JSON block.
3. Edit the target markdown file (e.g., `/home/user/docs/setup.md`) to prepend the extracted JSON block at the very top of the file, followed by a blank line, and then the original content.
4. Append a record of the update to a structured CSV file at `/home/user/docs/updated_registry.csv`. The CSV format must be: `FilePath,author,status` (e.g., `/home/user/docs/setup.md,jane.doe,draft`).
5. **Crucial:** Because other automated background processes occasionally write to `updated_registry.csv`, your Go script must acquire an exclusive file lock on the CSV file (using `syscall.Flock` with `syscall.LOCK_EX`) before appending the record, and unlock it afterward.

To execute your fix, you should run a shell command like:
`cat /home/user/docs_build.log | go run /home/user/fix_docs.go`

Ensure that the target markdown files are correctly updated and that the CSV file contains the correct records.