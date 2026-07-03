You are an AI assistant helping a technical writer organize a batch of unstructured documentation drafts.

The writer has dumped several draft files into the `/home/user/docs_incoming/` directory. These files are a mix of JSON (`.json`) and XML (`.xml`) formats containing documentation metadata and content. 

Your task is to write and execute a Python script `/home/user/organize_docs.py` that performs the following steps:
1. Iterates over all files in `/home/user/docs_incoming/`.
2. Parses each file based on its extension. 
   - For JSON files, extract the `author` and `doc_id` fields.
   - For XML files, extract the text inside the `<author>` and `<doc_id>` tags.
3. Moves and renames the file into `/home/user/docs_processed/` using the format: `{author}_{doc_id}.{ext}` (where `{ext}` is the original file extension). 
4. Ensure the incoming directory is empty after processing.

After running the script, you must create an incremental tar backup of the `/home/user/docs_processed/` directory. Save the backup as `/home/user/docs_backup/backup_1.tar` and store the snapshot (metadata) file for the incremental backup as `/home/user/docs_backup/snapshot.snar`. Use the standard `tar` command for this.

Directories:
- `/home/user/docs_incoming/` (Read files from here)
- `/home/user/docs_processed/` (Move and rename files here)
- `/home/user/docs_backup/` (Store the tar backup and snapshot here)

Ensure all directories exist before running your commands.