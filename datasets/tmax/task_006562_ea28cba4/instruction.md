You are acting as a technical writer's assistant. We have a pipeline where automated tools dump draft Markdown documentation into a specific directory. These drafts contain macros that need to be expanded, but because multiple automated systems might be writing to these files simultaneously, we need a robust, concurrent-safe watchdog daemon.

Your task is to write and run a Go program at `/home/user/doc_daemon.go` that does the following:

1. **Watch a Directory:** Use the `github.com/fsnotify/fsnotify` package to monitor the directory `/home/user/raw_docs/` for any `Create` or `Write` events on `.md` files.
2. **Safe Concurrent Access (File Locking):** When an event is detected for a file, your Go program must open the file and acquire an exclusive lock on it using `syscall.Flock` (`syscall.LOCK_EX`). This ensures that the automated system has finished writing its draft before you process it.
3. **Macro Application / Text Transformation:** Once the lock is acquired, read the file's content and apply the following text replacements:
   - Replace all occurrences of the macro `{{COMPANY_NAME}}` with `Acme Corp`.
   - Replace all occurrences of `{{STATUS}}` with `CONFIDENTIAL - DO NOT DISTRIBUTE`.
   - Append the exact string `\n\n---\nProcessed by DocWatchdog` to the end of the file.
4. **Output:** Write the transformed content to `/home/user/processed_docs/` using the exact same filename.
5. **Unlock:** Release the file lock (`syscall.LOCK_UN`) and close the input file.

**Environment Setup:**
- You must initialize a Go module named `docbot` in `/home/user/` and fetch the `fsnotify` dependency.
- Create the directories `/home/user/raw_docs/` and `/home/user/processed_docs/`.
- Start your Go program in the background (e.g., `go run /home/user/doc_daemon.go &`) and ensure it is actively watching.

**Testing Your Daemon:**
Once your daemon is running, manually create a file named `/home/user/raw_docs/test_doc.md` containing:
```markdown
# Welcome to {{COMPANY_NAME}}
This document is {{STATUS}}.
Please keep it safe.
```

If your program is correct, a properly transformed file will appear in `/home/user/processed_docs/test_doc.md`. Leave your program running in the background when you finish the task, as the automated evaluation will test its locking and watching capabilities by safely injecting files into `raw_docs`.