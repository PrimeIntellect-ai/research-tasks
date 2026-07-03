You are an AI assistant helping a technical writer organize a messy dump of legacy documentation and changelogs. 

Your task involves extracting nested archives, bulk renaming files to match our new style guide, and parsing a multi-line changelog to extract specific author contributions.

Please perform the following steps:

1. **Archive Extraction:**
   There is a nested archive at `/home/user/docs_archive.zip`. 
   Create a directory `/home/user/extracted_docs/` and unzip `docs_archive.zip` into it. 
   Inside, you will find a file named `drafts.tar.gz`. Extract its contents directly into `/home/user/extracted_docs/` (this will create a `drafts/` directory).

2. **Bulk Renaming:**
   Inside `/home/user/extracted_docs/drafts/`, there are several text files with spaces and uppercase letters. 
   Rename all `.txt` files in this directory to match standard markdown naming conventions:
   - Convert all letters to lowercase.
   - Replace all spaces with underscores (`_`).
   - Change the file extension from `.txt` to `.md`.
   *(Example: `API Spec Draft.txt` becomes `api_spec_draft.md`)*

3. **Multi-line Log Parsing & Format Conversion:**
   There is a changelog file at `/home/user/changelog.log`. Entries in this file are separated by a line containing exactly `---`. 
   A single log record looks like this:
   ```
   Commit: a1b2c3d
   Author: Alice Writer
   Date: 2023-10-12
   Message:
     Updated the authentication docs.
     Added OAuth2 examples.
   ```
   Parse this file and extract **only** the commits authored by `Alice Writer`. 
   Convert the extracted data into a valid JSON array and save it to `/home/user/alice_commits.json`.
   
   The JSON format must strictly be an array of objects, with the exact keys `commit`, `date`, and `message`. The `message` field should contain the trimmed message text (preserve the newlines between lines of the message, but remove the leading indentation). 
   
   Example output format:
   ```json
   [
     {
       "commit": "a1b2c3d",
       "date": "2023-10-12",
       "message": "Updated the authentication docs.\nAdded OAuth2 examples."
     }
   ]
   ```

Complete these tasks using Bash shell commands and scripts. Ensure the final JSON is perfectly formatted.