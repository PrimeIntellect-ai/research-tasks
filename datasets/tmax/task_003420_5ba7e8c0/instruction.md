You are helping organize a vast repository of legacy project files. Unfortunately, the repository has been contaminated with corrupted archives and files containing malicious macros.

Your task has two parts:

1. **Fix the Vendored Library**: 
We use a custom, proprietary library called `archivetool` to verify archive integrity. The source for this library is vendored at `/app/vendor/archivetool`. However, the previous developer introduced a bug in `archivetool/core.py` that causes it to crash immediately upon import or usage because of a missing environment variable. 
You must fix this library so it works without requiring any special environment variables, and install it into your Python environment.

2. **Create a Sanitizer Script**:
Write a Python script at `/home/user/sanitizer.py` that inspects a single file and determines if it is safe or malicious. The script must take exactly one argument (the file path) and exit with code `0` if the file is SAFE, and code `1` if the file is MALICIOUS.

The rules for classifying a file are:
* **Archives**: Use `archivetool.core.verify_archive(filepath)`. If the file is a recognized archive but fails verification (returns `False` or raises an exception), it is MALICIOUS. If it passes, it is SAFE.
* **Text Files**: If the file is not an archive, it is a text file. These files may be encoded in `UTF-8`, `UTF-16`, or `ISO-8859-1`. Your script must read the file, correctly detect or handle the encoding to decode it into a string, and check its contents. If the decoded text contains the exact string `[MALICIOUS_MACRO]`, it is MALICIOUS. Otherwise, it is SAFE.

Ensure your script is robust and correctly handles edge cases. We will run an automated test suite against `/home/user/sanitizer.py` using a large batch of clean and malicious files to verify your solution.