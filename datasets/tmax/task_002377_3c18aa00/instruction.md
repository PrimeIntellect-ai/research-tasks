You are an engineer for a technical writing team. The team receives documentation updates as compressed `.tar.gz` archives submitted by various remote writers. These archives are processed by a legacy, proprietary documentation compiler located at `/app/doc_compiler`. 

Unfortunately, `/app/doc_compiler` has two major issues:
1. It is highly vulnerable to archive extraction attacks (like path traversal and malicious symlinks).
2. It contains a hardcoded backdoor/debug flag that causes the compiler to overwrite system configuration if a specific string is present in any `.md` file's metadata block. 

Your task is to write a Python sanitization script at `/home/user/filter.py` that acts as a secure gatekeeper. 

The script must:
1. Accept a single command-line argument: the absolute path to a `.tar.gz` archive.
2. Safely inspect the contents of the archive (you may extract it to a temporary directory, but be sure to use secure extraction practices to avoid Zip-Slip/Tar-Slip attacks).
3. Ensure no files in the archive attempt to write outside the intended extraction directory (e.g., rejecting absolute paths, `../` sequences, or symlinks pointing outside the payload).
4. Inspect the contents of all `.md` files in the archive. You must reject any archive if *any* `.md` file contains the undocumented backdoor trigger string. You will need to analyze the stripped binary `/app/doc_compiler` to discover what this exact trigger string is.
5. Exit with code `0` if the archive is completely safe and clean.
6. Exit with code `1` if the archive is malicious or violates any safety checks.

Requirements:
- Your script must be written in Python 3.
- Use standard libraries (e.g., `tarfile`, `tempfile`).
- You must not modify `/app/doc_compiler` itself. 
- You must ensure that 100% of safe files are accepted, and 100% of malicious files are rejected.

The verification process will test your `/home/user/filter.py` against a hidden corpus of clean and malicious archives.