You are assisting a technical writer in organizing and migrating a dump of legacy documentation.

You have been provided with a nested archive located at `/home/user/legacy_docs.zip`.

Please perform the following steps to update the documentation:
1. Extract `/home/user/legacy_docs.zip` into a new directory at `/home/user/workspace`. 
2. Inside the extracted contents, you will find a tarball named `docs_archive.tar.gz`. Extract this tarball directly into `/home/user/workspace/` so that it creates a `/home/user/workspace/docs` directory.
3. Search through the extracted `/home/user/workspace/docs` directory (and all subdirectories) for all Markdown files (`*.md`) that contain the exact string `[DEPRECATED_MACRO]`.
4. For *only* those files that contain `[DEPRECATED_MACRO]`, perform an in-place text replacement to:
   - Replace all occurrences of `[DEPRECATED_MACRO]` with `[UPDATED_MACRO]`.
   - Replace all occurrences of the word `OldCorp` with `NewCorp`.
   (Do not modify markdown files that do not contain `[DEPRECATED_MACRO]`, even if they contain `OldCorp`).
5. Create a log file at `/home/user/migration.log`. This file must contain the absolute paths of all the files you modified, with one path per line, sorted alphabetically.

Ensure all file paths in your log file are absolute and correctly point to the extracted files.