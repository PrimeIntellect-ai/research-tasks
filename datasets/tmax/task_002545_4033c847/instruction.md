You are an AI assistant helping a developer organize a corrupted project backup.

You have a large text file located at `/home/user/archive.txt`. This file contains a mix of corrupted data, system logs, and valid project files that need to be extracted. 

Here are your instructions:

1. **Chunking**: First, use command-line tools to split `/home/user/archive.txt` into smaller chunks of exactly 15 lines each. Save these chunks in the directory `/home/user/chunks/` (which you must create) using the prefix `piece_`.
2. **Filtering & Merging**: Not all chunks contain valid data. Identify only the chunk files in `/home/user/chunks/` that contain the exact string `[VALID_BLOCK]`. 
3. **Piping to Python**: Concatenate these valid chunks in alphabetical order of their filenames, and pipe standard output directly into a Python script that you must write, located at `/home/user/extractor.py`.
4. **Extraction (Python Script)**: `/home/user/extractor.py` must read from standard input. The valid data stream will contain file boundaries formatted like this:
   `>>> PATH: <relative/path/to/file.txt> <<<`
   Followed by the file's contents, and ending with:
   `>>> END <<<`
   
   Your Python script must safely manipulate paths to reconstruct these files inside the base directory `/home/user/recovered_project/`. It should create any missing intermediate directories automatically. 
   *(Note: Discard any lines that are outside the `>>> PATH:` and `>>> END <<<` markers, including the `[VALID_BLOCK]` lines).*

**Verification:**
After running your pipeline, the automated test will check the contents of the files inside `/home/user/recovered_project/` to ensure they were correctly reassembled, chunked, merged, and path-manipulated. 

Do not run the script as root. All operations should be performed as the default user in `/home/user`.