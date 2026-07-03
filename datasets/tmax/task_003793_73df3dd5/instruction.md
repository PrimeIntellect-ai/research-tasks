You are an artifact manager responsible for curating binary repositories. You need to write a script that processes upload logs, decides which artifacts to keep based on their integrity, and generates a shell script to manage symbolic links and bulk renaming.

There is an image file located at `/app/policy.png`. This image contains a secret naming policy prefix (formatted as `PREFIX=<some_string>`). You must extract this prefix.

Write an executable program at `/home/user/generate_links.py` (you can use Python, Perl, Ruby, or Bash, but it must be executable) that reads a stream of multi-line log records from standard input (`stdin`) and prints a series of system commands to standard output (`stdout`).

The input consists of multiple records separated by a line containing exactly `===`.
Each record contains the following fields on separate lines (the order of fields within a record may vary):
`File: <filename without extension>`
`Ext: <extension, e.g., tar.gz>`
`Integrity: <VALID or CORRUPT>`

For each record:
- If `Integrity` is `VALID`, your program must print exactly:
  `ln -s /repo/<filename>.<Ext> /curated/<PREFIX><filename>.<Ext>`
  (Replace `<PREFIX>` with the actual prefix extracted from the image).
- If `Integrity` is `CORRUPT`, your program must print exactly:
  `rm -f /repo/<filename>.<Ext>`

Your program must handle an arbitrary number of records from `stdin` until EOF. Ignore leading/trailing whitespace on lines.

Constraints:
- You must create the executable script at `/home/user/generate_links.py`.
- Tesseract OCR is available if you need to read the image.
- Do not print anything else to `stdout` except the commands.