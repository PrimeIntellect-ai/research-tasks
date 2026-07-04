I am a technical writer managing a documentation library, and I need help automating my archival workflow. I regularly receive raw documentation archives that have lost their file extensions, and I need to process, format, and back them up using a configuration file.

Please write and execute a Bash script (or execute shell commands directly) to accomplish the following workflow:

1. **Read the Configuration:**
   I have a configuration file located at `/home/user/doc_rules.ini`. It defines four paths using the format `Key=Value`: `Incoming`, `Processed`, `Archives`, and `Snapshot`. Parse this file to determine the directories and files to use for the rest of the task. Create any of these directories if they do not already exist.

2. **Binary Format Extraction:**
   Inside the `Incoming` directory, there are several files without extensions (e.g., `doc_dump_1`, `doc_dump_2`). They are actually archives, but their exact types (`tar` or `tar.gz`) are unknown and must be identified programmatically (e.g., by checking their headers or using system utilities). 
   Extract the contents of all these archives directly into the `Processed` directory.

3. **Format Conversion:**
   The extracted archives contain Markdown (`.md`) files. In the `Processed` directory, find all `.md` files and convert them to plain text (`.txt`) files using the following rule:
   - Replace any Markdown header line starting with `# ` (a hash and a space) with `HEADER: ` (e.g., `# Introduction` becomes `HEADER: Introduction`).
   - Save the result with the same base name but a `.txt` extension (e.g., `intro.md` becomes `intro.txt`).
   - Delete the original `.md` files from the `Processed` directory.

4. **Incremental Backups:**
   Now that the documents are processed, perform a two-step incremental backup using GNU `tar`:
   - **Step A:** Create a level-0 (full) incremental tar backup of the `Processed` directory and save it as `backup_0.tar` in the `Archives` directory. You must use the snapshot file defined in `doc_rules.ini` to track the state.
   - **Step B:** Simulate a documentation update by creating a new file named `changelog.txt` in the `Processed` directory with the content `NEW UPDATE`.
   - **Step C:** Create a level-1 incremental backup of the `Processed` directory and save it as `backup_1.tar` in the `Archives` directory, reusing the same snapshot file.

All operations should be performed within `/home/user`. Ensure your backups properly capture the increment (i.e., `backup_1.tar` should only contain `changelog.txt` and the directory metadata, not the converted text files).