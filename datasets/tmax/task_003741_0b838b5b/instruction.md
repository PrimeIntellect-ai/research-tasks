You are assisting a technical writer who is organizing and compiling documentation for a massive legacy system. The documentation workflow relies on a proprietary, legacy documentation compiler located at `/app/doc_builder`. This binary is a stripped, black-box executable that takes markdown-like text, processes special custom include directives, and outputs compiled HTML.

Recently, the documentation repository was opened to community contributors. Unfortunately, some malicious users have submitted "evil" documents designed to crash the system, exfiltrate data, or cause infinite loops during compilation. 

Your task is to create a Python command-line utility, `/home/user/sanitize.py`, that acts as a security filter and pre-processor for these documents before they are fed to the compiler.

Here is the current system state and your requirements:
1. **Configuration Interpretation:** The technical writer has provided a configuration file at `/home/user/docs_config.ini` which specifies an `AllowedAssetDir` (which is `/home/user/docs/assets`).
2. **Symlink & Hardlink Management:** The documentation uses directives like `[[INCLUDE_ASSET: filename.ext]]`. The `doc_builder` blindly opens these files. Many of these assets are symlinks to shared code snippets. Your script must pre-resolve these symlinks. If a symlink loops infinitely, or resolves to a path outside the `AllowedAssetDir`, the document MUST be flagged as malicious and rejected.
3. **File Splitting & Piping:** The `doc_builder` binary has a strict buffer limit and crashes on inputs larger than 2KB. For any clean document, your script must split the file's text into 2048-byte chunks, pipe each chunk via standard input to `/app/doc_builder`, and merge the standard output streams back together.
4. **Atomic Writes:** The merged output must be written to an output directory. Because a live-reload web server monitors this directory, you must use atomic writes (writing to a temporary file and renaming it) so the server never reads a partially written file.

**Corpora Details:**
We have provided a corpus of contributor submissions to test your script:
- Clean corpus: `/home/user/corpus/clean/` (contains valid documents and safe asset links).
- Evil corpus: `/home/user/corpus/evil/` (contains path traversal includes, symlink bombs, and malformed data).

**Expected Usage:**
Your script must be executable and callable as:
`python3 /home/user/sanitize.py --input <path_to_doc> --outdir <path_to_output_dir>`

**Behavior:**
- If the document is malicious (violates configuration constraints, contains symlink loops, or attempts directory traversal via includes), your script must print an error to stderr, exit with code `1`, and NOT write any output file.
- If the document is clean, your script must safely chunk it, process it through `/app/doc_builder` via stdin/stdout redirection, atomically write the combined output to `<path_to_output_dir>/<original_filename>.html`, and exit with code `0`.

Analyze the `doc_builder` binary to understand its basic I/O expectations if needed. Ensure your final script handles all constraints flawlessly.