You are acting as an assistant for a technical writer who is organizing a large set of documentation notes.

The writer has a directory of incoming raw notes at `/home/user/raw_notes/`. Several background processes drop text files into this directory. 
Each text file contains one or more multi-line log records formatted exactly like this:

```
Title: <title>
Date: <YYYY-MM-DD>
Body:
<multi-line text here>
===END===
```

You need to write and execute a Python script at `/home/user/compile_docs.py` that consolidates all these notes into a single Markdown document at `/home/user/compiled_docs.md`.

Because background processes might attempt to read or write the compiled documentation at any moment, your script MUST guarantee safe concurrent access and atomic updates. 

Your script must perform the following:
1. Parse all multi-line log records from all `.txt` files in `/home/user/raw_notes/`.
2. Reformat each record into the following Markdown format:
```
## <title>
*<date>*

<body>
```
3. Sort the reformatted records chronologically by Date (oldest first). If dates are identical, preserve the original order they were read.
4. Join the sorted records with a single blank line between them.
5. Safely update `/home/user/compiled_docs.md` using the following strict concurrent access pattern:
    - Open and acquire an exclusive file lock (`fcntl.flock`) on a dedicated lock file: `/home/user/docs.lock`.
    - Create a temporary file in `/home/user/` and write the fully compiled Markdown string to it.
    - Atomically replace `/home/user/compiled_docs.md` with the temporary file (e.g., using `os.replace`).
    - Release the lock.

Write the script, ensure it has executable permissions, and run it once so that `/home/user/compiled_docs.md` is generated.