You are acting as an AI assistant for a technical writer who needs to reorganize and update a massive, legacy documentation archive.

In `/home/user/docs_archive.tar.gz`, there is a large collection of Markdown documentation files. 
Your objective is to locate specific outdated files based on their metadata, apply a large-scale text update to them using memory-efficient I/O, repackage them, and serve the results.

Please complete the following phases:

1. **Metadata-based Search & Memory-Efficient Editing:**
   Write and run a Python script to process the files. You must find all `.md` files that contain the exact string `Version: 1.0` in their first 5 lines (the metadata header).
   For only these matching files, you must:
   - Use memory-mapped I/O (`mmap`) or streaming line-by-line reading to process the files without loading the entire file into memory at once.
   - Change the metadata line `Status: Active` to `Status: Deprecated` (if it exists).
   - Find all occurrences of the legacy API URL `http://api.old.local/v1/` and replace them with `https://api.new.local/v2/`.

2. **Reporting:**
   Your Python script must generate a JSON report at `/home/user/update_report.json`.
   The JSON must be a single dictionary mapping the relative file path (e.g., `docs/section1/file.md`) to the integer number of API URL replacements made in that specific file.
   Only include files that had `Version: 1.0` in the report.

3. **Archiving:**
   Package ONLY the modified files into a new archive at `/home/user/updated_docs.tar.gz`. Maintain their original relative directory structure (e.g., `docs/...`).

4. **Service:**
   Start a simple background HTTP server using Python on port 8080, serving the `/home/user` directory, so that the technical writer can download the report and the new archive. Leave it running in the background.

Ensure all file paths and exact strings match the instructions.