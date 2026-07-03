You are assisting a technical writer in migrating and organizing an old documentation archive. You have been provided with an archive located at `/home/user/docs_archive.tar.gz`.

Your task is to write and execute a Bash script to process these files according to the following strict requirements:

1. Extract the contents of `/home/user/docs_archive.tar.gz` into a temporary directory `/home/user/docs`.
2. Create a target directory at `/home/user/docs_processed`.
3. The extracted archive contains several text-based documentation files with inconsistent naming conventions and extensions (e.g., `.TXT`, `.Txt`, `.text`). Find all such files. For each file, extract the numeric digits from its filename. Copy the file into `/home/user/docs_processed/` renaming it to the format `doc_<digits>.md`. (For example, a file named `Draft-04.Txt` should be copied as `doc_04.md`).
4. Append the exact string `\n[END OF DOCUMENT]` (a newline followed by the bracketed text) to the end of every `.md` file in `/home/user/docs_processed/`.
5. The extracted archive also contains base64-encoded binary assets with the `.b64` extension. Decode each of these files from base64 and save the output as a binary file in `/home/user/docs_processed/`, preserving the base filename but changing the extension to `.bin` (e.g., `asset_1.b64` becomes `asset_1.bin`).
6. Finally, package all the processed files in `/home/user/docs_processed/` into a new compressed tarball located at `/home/user/final_docs.tar.gz`. The files must be at the root of the archive (do not include the `docs_processed/` directory itself in the archive paths).

Ensure your script handles all files programmatically and handles formatting dynamically using Bash.