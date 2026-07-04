You are assisting a technical writer who is organizing a massive stream of automated API documentation. An automated generator is running in the background, continuously writing markdown files to a directory. 

We need to safely process these files as they arrive, redact sensitive information, compress them into a custom single-file archive stream, and keep a precise manifest. Because the generator is actively writing, you must handle potential race conditions (the generator writes to `.tmp` files and then renames them to `.md` when finished).

Here is your task:
1. Create a Python script at `/home/user/processor.py` to process the documentation files.
2. The generator is dropping files into `/home/user/incoming_docs/`.
3. Your script should continuously monitor `/home/user/incoming_docs/` for files ending in `.md`.
4. For each `.md` file found:
   a. Read the contents.
   b. Replace all instances of the exact string `INTERNAL_CONFIDENTIAL` with `[REDACTED]`.
   c. Calculate the SHA-256 checksum of the transformed text (as a hex string).
   d. Compress the transformed text using Python's standard `zlib.compress()` (use default compression level).
   e. Append the compressed binary payload to `/home/user/archive/docs.archive`.
   f. Append a record to the manifest file at `/home/user/archive/manifest.csv` in the exact following format:
      `filename,sha256_hex,byte_offset_in_archive,compressed_size_in_bytes`
      *(Example: `api_001.md,e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855,0,125`)*
   g. Delete the processed `.md` file from `incoming_docs`.
5. Run your script. A background process will generate exactly 50 files (named `doc_01.md` through `doc_50.md`). Ensure your script processes all 50 files and then you can terminate it.
6. Create `/home/user/archive/` before starting.
7. Ensure `manifest.csv` has no header row, just the data rows.

Please create the directories, write the script, start the background generator (if I had provided the command, but since it's already running in the environment, just run your processor until the incoming directory has been empty for a few seconds and 50 files are in the manifest), and exit gracefully once done.

*(Note: The generator script `/home/user/generator.sh` is available if you need to manually trigger it, run it in the background: `bash /home/user/generator.sh &`)*