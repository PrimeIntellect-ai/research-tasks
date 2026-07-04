I have a messy project directory located at `/app/messy_project` that needs to be reorganized and packaged. 

First, there is an image file at `/app/schema.png` which contains the text of the required directory structure and file categorization rules (e.g., which file extensions go into which folders). Please extract this text.

Next, write a Python script at `/home/user/organize.py` that performs the following:
1. Reads the extracted schema rules.
2. Recursively traverses `/app/messy_project` and searches for files based on their metadata (e.g., extension, size).
3. Moves and renames files into a new directory structure at `/home/user/organized_project` according to the rules in the schema.
4. Converts any `.txt` log files to `.json` format, extracting the timestamp and message.
5. Generates a manifest file at `/home/user/organized_project/manifest.json` containing the relative paths and SHA-256 checksums of all organized files.
6. Compresses the entire `/home/user/organized_project` directory into a tarball at `/home/user/project.tar.gz`.

Ensure your Python script runs successfully and creates the final archive. An automated test will evaluate the correctness of your organization by computing the F1 score of the correctly placed files and checksums in your manifest against our reference manifest. Your F1 score must be at least 0.95.