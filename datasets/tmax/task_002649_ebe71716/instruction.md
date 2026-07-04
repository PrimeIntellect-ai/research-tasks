You are an AI assistant helping a technical writer organize and verify a large documentation repository. 

Our team uses a custom documentation manifest format to track which files are included in our final publishing build. Unfortunately, the exact configuration parameters (base directory and hash salt) were lost in a wiki crash, but we managed to recover a screenshot of the configuration specs, located at `/app/config_spec.png`.

Your task is to:
1. Extract the missing configuration parameters (the Base Directory and the Hash Salt) from the image `/app/config_spec.png`. You can use `tesseract` to read the image.
2. Write a Go program at `/home/user/doc_builder.go` and compile it to `/home/user/doc_builder`.
3. The program must act as a manifest parser and checksum generator. It will be tested against an automated suite that generates thousands of random manifest files to ensure absolute compliance with our internal standard.

**Manifest Parser Specification:**
- The program must read line-by-line from standard input (`stdin`).
- Empty lines and lines starting with `#` (after trimming leading/trailing whitespace) must be ignored.
- Valid lines start with either `+ ` (include) or `- ` (exclude), followed by a file path. (Note the space after the `+` or `-`).
- The file paths might be absolute or relative. If a path is relative (does not start with `/`), it must be resolved against the **Base Directory** recovered from the image. Path elements like `.` and `..` must be cleanly resolved (e.g., `/opt/techdocs/./api/../intro.md` becomes `/opt/techdocs/intro.md`).
- If a path is explicitly excluded (`- `), it must be removed from the final list of included files, even if it was included earlier. If it is included again later, it is added back. 
- The final output must be printed to standard output (`stdout`), containing only the currently included files.
- The output must be sorted alphabetically by the absolute resolved path.
- Each line in the output must be formatted exactly as: `<SHA256> <ABSOLUTE_PATH>`
- The `<SHA256>` is the hex-encoded SHA-256 hash of the exact string: `[ABSOLUTE_PATH][SALT]` (where `[SALT]` is the Hash Salt recovered from the image). Note: Do not hash the contents of the file, just the string path concatenated with the salt.

Build your Go program and place the executable at `/home/user/doc_builder`. Make sure it works perfectly, as it will be subjected to intensive fuzz-testing against a reference implementation.