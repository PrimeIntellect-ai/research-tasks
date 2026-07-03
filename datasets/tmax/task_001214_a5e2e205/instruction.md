I am a technical writer organizing some legacy documentation. My predecessor stored several drafts in a custom concatenated text format instead of a standard archive. I need you to extract the files, clean up their names, and package them properly.

Here is what you need to do:
1. You will find a file at `/home/user/legacy_docs.txt`. This file contains multiple markdown documents.
2. The custom format uses the following structure for each file:
   - A header line specifying the filename: `===FILE:<filename>===`
   - The contents of the file.
   - A footer line indicating the end of the file: `===EOF===`
   Extract all the files into a new directory `/home/user/extracted/`.
3. The extracted files will have names like `Draft_v1_intro.md` or `Draft_v7_api_reference.md`. Perform a bulk rename on these files to remove the `Draft_v<number>_` prefix, leaving just the core names (e.g., `intro.md`, `api_reference.md`).
4. Finally, compress all the renamed files into a standard gzip-compressed tarball at `/home/user/final_docs.tar.gz`. The tarball should contain *only* the files themselves, not the `extracted` directory structure.
5. **Crucial:** To prevent partial reads by other automated systems, you must use an atomic write for the final archive. Create the `.tar.gz` in a temporary location (e.g., using `mktemp`) and then atomically move (`mv`) it to `/home/user/final_docs.tar.gz`.

Complete these steps using Bash commands or a Bash script.