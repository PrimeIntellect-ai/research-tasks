As an incident responder, you are investigating a web server that was recently compromised via a path traversal vulnerability in its file upload handler. The attacker left behind a taunting image at `/app/attacker_note.png`. 

Your task is to write a robust Python path-traversal detector that can filter out malicious filenames, incorporating a specific secret word left by the attacker in the image.

1. Use OCR (e.g., `tesseract`) to extract the secret uppercase word from `/app/attacker_note.png`.
2. Create a Python script at `/home/user/detector.py`. 
3. The script must accept a single command-line argument: the filename to check.
    - Example invocation: `python3 /home/user/detector.py "report.pdf"`
4. The script must validate the filename to prevent path traversal. It should catch:
    - Absolute paths (e.g., `/etc/passwd`)
    - Directory climbing sequences (`../`, `..\`)
    - Null bytes (`\0`, `%00`)
    - URL-encoded, double-URL-encoded, and Unicode variants of dots and slashes (e.g., `%2e%2e%2f`, `%252e%252e%252f`, `..%c0%af`)
5. If the filename is completely safe (a simple file name with no directory components or traversal attempts), the script must print exactly `SAFE` to stdout and exit with status code `0`.
6. If the filename contains any path traversal attempt or malicious characters, the script must print `REJECTED_<SECRET_WORD>` (replacing `<SECRET_WORD>` with the exact uppercase word extracted from the image, stripped of whitespace) to stdout and exit with status code `1`.

Your script will be tested against a large corpus of clean filenames and a corpus of known path-traversal evasion payloads. You must correctly classify 100% of both corpora.