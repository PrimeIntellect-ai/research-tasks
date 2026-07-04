My development team uses a proprietary archive format called `.pka` (Project Kontainer Archive) to package and organize large datasets and project dependencies. We use a legacy extraction utility located at `/app/pka_extract` to unpack these files. Unfortunately, the source code for this utility was lost, and the compiled binary is completely stripped.

We recently discovered that `/app/pka_extract` is vulnerable to arbitrary file overwrites (Zip Slip) and malicious symlink attacks. It blindly extracts files to paths contained in the archive, meaning a maliciously crafted `.pka` file can overwrite critical system files or place files outside the intended project directory using absolute paths (`/`), directory traversal (`../`), or by extracting symlinks that point outside the root directory.

We cannot replace `/app/pka_extract` right now. Instead, I need you to create a Python-based gatekeeper script at `/home/user/pka_guard.py`. This script will act as an integrity and security verifier that checks a `.pka` file *before* we pass it to the extractor.

Your task:
1. Figure out the binary structure of `.pka` files. You can reverse-engineer `/app/pka_extract` (using tools like `strings`, `xxd`, `objdump`, or `gdb`) or inspect the two sample `.pka` files I have left in `/home/user/samples/` (`safe.pka` and `malicious.pka`).
2. Write `/home/user/pka_guard.py` which takes exactly one CLI argument: the path to a `.pka` file.
   Usage: `python3 /home/user/pka_guard.py <path_to_pka_file>`
3. The script must parse the archive format in pure Python without calling the external `pka_extract` binary.
4. The script must exit with status code `0` if the archive is completely safe to extract.
5. The script must exit with status code `1` (or any non-zero) if the archive contains ANY of the following:
   - Absolute file/directory paths (starting with `/`).
   - Path traversals that would resolve outside the extraction root (e.g., `foo/../../etc/passwd`).
   - Symlinks whose target points outside the extraction root, either via absolute paths or traversal.
6. The script should be robust enough to handle large-scale macro applications and massive project archives without running out of memory (do not load massive file contents into memory; you only need to parse the metadata/headers and symlink targets).

Remember, you must write the parsing logic yourself in Python based on your understanding of the format. Create the `/home/user/pka_guard.py` script and make sure it is executable.