I am a technical writer managing our documentation portal, and our latest site build failed. I need your help to parse the build logs, locate the failing files, and generate a structured summary report so I know who to contact to fix them.

Here is the situation:
1. We have a multi-line log file at `/home/user/build_errors.log`. When a document fails to build, the log outputs a multi-line error block that looks exactly like this:
```
[ERROR] Build interrupted.
File: /home/user/docs/networking.md
Reason: Broken internal hyperlink
```
(Note: There may be other unrelated log lines between or around these error blocks).

2. All our documentation files are located in `/home/user/docs/`. These are Markdown files (`.md`) that begin with a YAML frontmatter block containing metadata, like this:
```markdown
---
Author: Jane Doe
Topic: Networking
---
# Content starts here...
```

Your task is to:
1. Parse `/home/user/build_errors.log` to find all files that failed the build and the specific `Reason` for the failure.
2. For each failed file, read its corresponding Markdown file in `/home/user/docs/` and extract the `Author` from the frontmatter.
3. Combine this information and create a consolidated JSON file at `/home/user/failed_docs_summary.json`.

The output file `/home/user/failed_docs_summary.json` must be a single JSON object where the keys are the **base filenames** (e.g., `networking.md`) and the values are objects containing the `author` and `reason`. 

Example of expected output format in `/home/user/failed_docs_summary.json`:
```json
{
  "networking.md": {
    "author": "Jane Doe",
    "reason": "Broken internal hyperlink"
  },
  "api_v2.md": {
    "author": "John Smith",
    "reason": "Missing alt text for image"
  }
}
```

You can use any language available (like Python, Node.js, bash, etc.) to write a script to achieve this.