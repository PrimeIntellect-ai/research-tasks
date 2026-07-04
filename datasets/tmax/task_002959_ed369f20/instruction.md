You are an artifact manager tasked with processing a repository of custom binary archives. The system receives archives that sometimes contain malicious paths intended to overwrite system files (a vulnerability known as "zip slip").

You need to perform a multi-stage curation and write a precise sanitization script.

**Step 1: Locate and Rename Artifacts**
Find all files in `/app/incoming` that have the `.dat` extension and were modified within the last 7 days. Bulk rename all of these files to have the `.car` (Custom Archive) extension.

**Step 2: Extract Security Policy**
There is a security policy image located at `/app/policy.png`. Extract the text from this image (you may use `tesseract`). The image contains a "Base Directory" path that must be used as the root for all extractions.

**Step 3: Write a Manifest Sanitizer (`/home/user/safe_manifest_parser.py`)**
The archives use a custom structured format. The metadata of these archives is a JSON array of file entries, representing the contents. You must write a Python script that reads this JSON array from standard input (`stdin`) and prints the safe absolute paths.

Your script `/home/user/safe_manifest_parser.py` must strictly obey these rules:
1. It reads a JSON string from `stdin`. The JSON is a list of dictionaries, each containing at least a `"path"` string key. Example: `[{"path": "docs/readme.txt"}, {"path": "../../etc/passwd"}]`
2. For each entry, resolve the absolute path as if it were being extracted into the "Base Directory" you found in the image.
3. **Zip-slip prevention:** If the resolved absolute path does not strictly start with the Base Directory path (meaning it tries to escape the directory via `../` or absolute path injection), it must be rejected.
4. Output format: For each entry in the JSON array (in the original order), print exactly one line to standard output.
   - If the path is safe, print the absolute resolved path.
   - If the path is unsafe (escapes the base directory), print: `REJECTED: <original_path>`

*Note: Your script will be tested against thousands of edge cases by an automated fuzzing verifier to ensure it exactly matches the behavior of our secure reference implementation. Make sure it properly handles paths with multiple `../`, `/`, `./`, and absolute path attempts.*