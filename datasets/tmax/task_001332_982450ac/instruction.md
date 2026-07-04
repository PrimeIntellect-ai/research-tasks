You are assisting a technical writer who is migrating a massive library of legacy documentation. The legacy documents are stored in a nested archive format, and they contain obsolete company references that need to be updated. 

The original documentation dump is located at `/home/user/legacy_docs.tar`.
Inside this uncompressed tarball, there are several `.zip` files (e.g., `set1.zip`, `set2.zip`).
Inside these zip files are thousands of documentation files.

However, the archive is messy and contains irrelevant files. You only want to process valid technical documents. Valid technical documents are identifiable by a specific 8-byte binary header: `b'TECHDOC\x00'`. 

Your task is to write and execute a Python script at `/home/user/migrate_docs.py` that does the following:
1. Opens `/home/user/legacy_docs.tar` and streams/reads the `.zip` files inside it.
2. Reads the files inside each `.zip` without extracting the entire archives to disk (use memory/streaming).
3. Checks each file for the 8-byte binary magic header `b'TECHDOC\x00'`. 
4. If the file has this header, skip the header, decode the remaining bytes as `utf-8` text.
5. Perform a text replacement: replace all instances of the exact string `[COMPANY_V1]` with `OmniCorp`.
6. Write the processed text (encoded back to `utf-8`, WITHOUT the 8-byte binary header) into a new, flattened zip archive at `/home/user/clean_docs.zip`.
7. The filenames inside `/home/user/clean_docs.zip` should be formatted as `{name_of_zip_file}_{name_of_document_file}` (e.g., `set1.zip_doc1.txt`).
8. To ensure data integrity, your script MUST write the new zip to a temporary file first (e.g., `/home/user/clean_docs_temp.zip`) and use an atomic rename operation (`os.replace` or `shutil.move`) to finalize it to `/home/user/clean_docs.zip`.
9. Finally, append a summary line to `/home/user/migration.log` in the format: `Migration complete. Processed X valid documents.` (where X is the integer count).

Write the Python script, execute it, and verify the output.