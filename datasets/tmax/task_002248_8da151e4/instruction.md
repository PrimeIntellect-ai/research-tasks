You are an on-call engineer who just received a 3 AM page. The legacy data ingestion pipeline has completely halted. 

The pipeline uses a compiled C utility that crashes and corrupts its temporary database whenever it encounters improperly formatted filenames, specifically triggering an off-by-one buffer overflow and failing to handle string boundaries correctly.

Unfortunately, the original developer left no text documentation. The only surviving specification of the exact boundary conditions for valid filenames is a screenshot of an old Slack message, located at `/app/legacy_rule.png`.

Your task is to:
1. Examine `/app/legacy_rule.png` (using OCR tools like `tesseract` which is pre-installed) to determine the exact boundary rules for valid filenames.
2. Create a robust Python sanitizer script at `/home/user/sanitizer.py` that can filter out malicious or crashing filenames before they reach the C utility.

The script must:
- Accept a single filename string as a command-line argument: `python3 /home/user/sanitizer.py "<filename>"`
- Only evaluate the basename of the file, ignoring any directory paths if provided.
- Exit with status code `0` if the filename is completely valid according to the legacy rules.
- Exit with status code `1` if the filename violates the rules (e.g., contains forbidden characters or violates the boundary limit).

You must use the exact rules extracted from the image to repair this pipeline. Ensure your script handles edge cases robustly, as the automated test pipeline will run your script against a hidden adversarial corpus of "evil" filenames and a "clean" corpus of valid ones.