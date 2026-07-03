You are an AI assistant helping a technical writer securely process automated documentation submissions.

We receive documentation updates in various structured formats (JSON, CSV, XML) packed in a compressed tarball archive. Recently, we discovered that some automated submission systems are misconfigured, resulting in archives containing absolute paths or relative path traversal sequences (e.g., `../`). This is a serious security risk known as "Tar Slip".

Your task is to write and execute a Python script at `/home/user/build_docs.py` that performs the following steps:

1. **Secure Extraction**: Read the archive located at `/home/user/incoming_docs.tar.gz`. Extract its contents to `/home/user/docs_raw`. 
   - You MUST implement a security check in your Python script to prevent Path Traversal/Tar Slip. 
   - Iterate through the archive members. If a member's target extraction path resolves to a location strictly outside of the absolute path of `/home/user/docs_raw`, you must **skip** it.
   - Do not use any third-party CLI tools (like standard `tar` command) for extraction, you must do it programmatically in Python.

2. **Format Conversion**: The valid extracted files will be in JSON, CSV, and XML formats. Parse each file in `/home/user/docs_raw` and convert them into Markdown files, saving the outputs to `/home/user/docs_md/`. 
   - All source files contain documentation records with `title` and `content` fields.
   - For a record with title "My Doc" and content "Some text", the output file should be named exactly `<title>.md` (spaces replaced by underscores, e.g., `My_Doc.md`).
   - The contents of the markdown file should be exactly:
     ```markdown
     # <title>
     
     <content>
     ```
   - **JSON Format**: An array of objects: `[{"title": "Doc A", "content": "Text A"}]`
   - **CSV Format**: Header row `title,content`, followed by data rows.
   - **XML Format**: `<docs><doc><title>Doc C</title><content>Text C</content></doc></docs>`

3. **Reporting**: After processing, generate a JSON report at `/home/user/report.json` with the following exact keys:
   - `"skipped_members"`: The integer count of archive members that were skipped due to the path traversal security check.
   - `"extracted_files"`: The integer count of valid files successfully extracted to `/home/user/docs_raw`.
   - `"generated_md_files"`: The integer count of markdown files successfully created in `/home/user/docs_md`.

Ensure all necessary output directories are created by your script if they don't exist.
Run your script and ensure the final state (`/home/user/docs_md/` and `/home/user/report.json`) is successfully generated.