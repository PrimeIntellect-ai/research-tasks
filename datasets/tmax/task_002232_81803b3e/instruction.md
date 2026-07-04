You are an AI assistant helping a technical writer organize a chaotic documentation repository. 

The writer has a directory of finalized markdown files in `/home/user/raw_docs/`. However, the filenames in this directory have been updated over time, and they no longer match the filenames originally planned in the site structure. 

The desired website structure is defined in a JSON file at `/home/user/sitemap.json`. This file contains nested dictionaries where the top-level keys are category folders, the second-level keys are the article titles, and the values are the *original* markdown filenames.

To map the original filenames to the current, finalized filenames, the writer has provided a multi-line migration log at `/home/user/migration.log`. Each record in the log spans multiple lines and follows this exact format, separated by blank lines:

```
[TIMESTAMP] UPDATE
Original: <old_filename>
New: <current_filename>
Reason: <reason text>
```

Your task is to write a Python script (or use shell commands) to perform the following:
1. Parse `/home/user/sitemap.json` and `/home/user/migration.log`.
2. Map the original filenames in the JSON to their corresponding new filenames found in the `migration.log`.
3. Create a new directory tree at `/home/user/docs_portal/`.
4. Inside `/home/user/docs_portal/`, create the category folders defined in the JSON.
5. Inside each category folder, create a **symbolic link** for each article. The name of the symbolic link must be the article title (the second-level key in the JSON) with a `.md` extension. The symbolic link must point to the absolute path of the correct current filename in `/home/user/raw_docs/`.

For example, if the JSON has `{"API": {"v1": "api_v1.md"}}` and the log maps `api_v1.md` to `api_v1_final.md`, you should create a symlink at `/home/user/docs_portal/API/v1.md` pointing to `/home/user/raw_docs/api_v1_final.md`.

Ensure all symlinks are valid and point to the correct files.