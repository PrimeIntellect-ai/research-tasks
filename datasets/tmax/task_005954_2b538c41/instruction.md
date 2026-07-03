You are assisting a technical writer who is migrating a legacy documentation archive to a new organized structure. The archive contains old documentation files scattered across various subdirectories, and they are all individually compressed. 

Here is the current state of the system:
1. You have a directory called `/home/user/docs_archive/`. Inside, there are several nested directories containing compressed text files (e.g., `file_A.txt.gz`, `file_B.txt.gz`).
2. You have a CSV index file at `/home/user/docs_index.csv`. The CSV has no header and uses the format: `original_filename,target_category,new_filename` (e.g., `file_A.txt.gz,API_Reference,auth_endpoints`).

Your objective is to process these files using only standard Bash commands and Coreutils:
1. Read `/home/user/docs_index.csv`.
2. For each entry, recursively locate the `original_filename` inside `/home/user/docs_archive/`.
3. Decompress the file.
4. The legacy docs contain an outdated macro placeholder: `[MACRO:COMPANY_NAME]`. You must perform a text replacement to change every instance of `[MACRO:COMPANY_NAME]` to `GlobalTech`.
5. Save the updated text to a new directory structure: `/home/user/new_docs/<target_category>/<new_filename>.txt`. You will need to create the `new_docs` directory and the category subdirectories as needed.
6. Once all files have been processed, create a compressed tarball of the entire `/home/user/new_docs/` directory at `/home/user/release.tar.gz`. The tarball should contain the `new_docs` directory at its root.
7. Finally, create a log file at `/home/user/migration.log` containing just the `<new_filename>.txt` of every file you successfully processed, with one filename per line, sorted alphabetically.

Constraints:
- You must use Bash shell commands, Coreutils, and standard CLI tools (like `sed`, `awk`, `find`, `tar`, `gzip`). Do not use Python, Perl, or other scripting languages.
- Only process files listed in the CSV. Ignore any other files in the archive.