You need to build a secure Go-based log organizer utility that processes compressed log archives, standardizes their filenames, and defends against malicious archive attacks.

We receive log drops in `.tar.gz` format from various internal systems. Recently, a red team demonstrated that our current extraction scripts are vulnerable to path traversal attacks (e.g., archive entries containing `../` or absolute paths like `/etc/shadow`), which race against our file watchers.

Your task is to write a Go program `/home/user/log_organizer.go` that safely processes these archives. 

Requirements for your Go program:
1. It must be a CLI tool compiled to `/home/user/log_organizer`.
2. It should accept two arguments: an input `.tar.gz` file path and an output directory path. Example: `./log_organizer input.tar.gz /tmp/out`
3. It must stream and parse the `.tar.gz` file (Compressed stream processing).
4. **Sanitization**: It must analyze the header of every file in the archive. If ANY file in the archive contains a path traversal sequence (`../` or `..\`) or is an absolute path (starts with `/`), the program MUST reject the entire archive, print "MALICIOUS ARCHIVE", exit with a non-zero status code, and ensure nothing is left in the output directory.
5. **Renaming**: If the archive is safe, it should extract the files (handling recursive directory traversal within the tar) and bulk-rename them. 
6. **Formatting Rule**: The target format for the renamed files is stored in an image file at `/app/target_format.png`. You will need to extract the text from this image (e.g., using `tesseract`) to discover the exact prefix and naming convention required for the extracted logs. All extracted `.log` files must be renamed to match this exact format string pattern (replacing the placeholders with the original file's base name, stripped of its old extension).

Ensure your Go application is robust. We will test it against a set of clean archives (which must be processed and renamed successfully) and a set of adversarial archives (which must be completely rejected).