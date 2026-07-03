You are an AI assistant helping a technical writer organize a messy dump of documentation from various engineering teams.

You have been given a nested archive located at `/home/user/raw_docs.tar.gz`. This archive contains a directory tree with further archives (`.zip`, `.tar.gz`, etc.) inside it, which in turn contain documentation files. 

Your goal is to extract all the documentation, fix file names and extensions, update outdated company terms inside the text, create a verified manifest, and package everything into a final clean archive.

Here are your specific instructions:

1. **Extraction**: Extract `/home/user/raw_docs.tar.gz` into `/home/user/docs_processed/`. Traverse the extracted directory and extract any nested archives you find into their respective current directories. Once extracted, delete the nested archive files (e.g., the inner `.zip` or `.tar.gz` files) so only the directories and text/markdown files remain.

2. **Bulk Renaming**: 
   - Change all file extensions ending in `.txt.old` or `.md.draft` to `.md`.
   - Rename all documentation files so their basenames are strictly lowercase and any spaces are replaced with dashes (`-`). For example, `API Specs.txt.old` should become `api-specs.md`.

3. **Text Transformation**: 
   - Across all the resulting `.md` files, replace all occurrences of the exact string `AcmeCorp` with `GlobalTech`.
   - Replace all occurrences of the exact string `Draft: Yes` with `Status: Published`.
   - You must use Bash utilities (like `sed`, `awk`, etc.) to do this in-place or by replacing the files.

4. **Manifest Generation**: 
   - Create a manifest file at `/home/user/doc_manifest.csv`.
   - The file must contain a list of all the final `.md` files in the format: `relative/path/to/file.md,SHA256_CHECKSUM`
   - The paths must be relative to the `/home/user/docs_processed/` directory (e.g., `engineering/backend/api-specs.md`).
   - The manifest must be sorted alphabetically by the file path.

5. **Re-archiving**:
   - Create a final archive at `/home/user/published_docs.tar.gz` containing the contents of `/home/user/docs_processed/`. When extracting this new archive, it should immediately yield the top-level directories/files that were inside `docs_processed`, without a redundant top-level wrapper folder.

Ensure that your final manifest and archive exactly match the requested specifications.