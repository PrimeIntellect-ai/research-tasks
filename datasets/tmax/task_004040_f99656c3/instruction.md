You are helping a technical writer process a large, unverified documentation archive provided by an external vendor. The vendor is known for poorly constructed archives that sometimes suffer from "Zip Slip" vulnerabilities (where files try to extract outside the intended directory using `../` path traversal).

First, the lead writer has left an audio note for you at `/app/dictation.wav`. You need to listen to this (transcribe it) to find out the **exact name of the secret root directory** where the documentation must be stored. 

Next, you need to write a standalone C++ program that will safely resolve and sanitize a list of archive file paths to prevent Zip Slip. 

Write the C++ source code at `/home/user/path_resolver.cpp` and compile it to `/home/user/path_resolver`.

Your C++ program must meet these strict requirements:
1. It reads file paths from standard input (`stdin`), one path per line.
2. For each path, it evaluates the directory traversal logically component by component (split by `/`).
3. Rules for evaluation:
   - Ignore empty components (e.g., `//` is treated as `/`) and `.` components.
   - A `..` component means navigating up one directory level. 
   - Leading slashes `/` are ignored (i.e., the path is treated as relative to the secret root).
   - If a `..` component attempts to navigate *above* the secret root directory (i.e., navigating up when already at the root), the entire path is malicious. You must output exactly `INVALID` for this line.
   - If the path is valid, output the final resolved path by joining the remaining components with `/`, prefixed by the secret root directory name and a trailing slash. If the resolved path points exactly to the root directory, just output the secret root directory name with a trailing slash.

**Example scenarios (assuming the secret root directory from the audio was `my_secret_docs`):**
- Input: `docs/../images/logo.png` 
  Output: `my_secret_docs/images/logo.png`
- Input: `/var/www/html/index.html`
  Output: `my_secret_docs/var/www/html/index.html`
- Input: `intro/../../etc/passwd`
  Output: `INVALID`
- Input: `a/./b/../../c.txt`
  Output: `my_secret_docs/c.txt`
- Input: `.`
  Output: `my_secret_docs/`

Your program must process `stdin` until EOF and write to `stdout`, line for line. Do not print any extraneous text. We will test your compiled binary with an automated suite of thousands of path mutations.