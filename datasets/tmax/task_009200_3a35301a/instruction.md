You are an artifact manager responsible for curating binary repositories. You have been given a staging directory containing newly uploaded files, but the directory is messy and contains a mix of executable binaries, non-executable files, and debug builds.

Your task is to generate a clean, validated manifest of production-ready binaries.

Here are your instructions:

1. **Find Target Files**: Search the directory `/home/user/artifacts/` for all files that meet **both** of the following criteria:
   - The file extension is `.bin`
   - The file has executable permissions

2. **Generate Initial Manifest**: Create a file at `/home/user/manifest.csv` containing metadata for the files you found. 
   - Each line in the CSV must correspond to one file and follow this exact format: `filename,size_in_bytes,sha256_checksum`
   - Note: Use only the base filename (e.g., `app.bin`), not the full path.
   - Sort the lines alphabetically by filename.

3. **Fix the Curation Tool**: There is a C program located at `/home/user/clean_manifest.c`. Its purpose is to read an initial manifest from standard input, filter out any binaries whose filename contains the word "debug" (as these should not go to production), and print the remaining valid lines to standard output.
   - However, the original developer made a critical memory management error in `clean_manifest.c` that causes a segmentation fault / double-free error when processing multiple lines.
   - Find and fix the bug in `/home/user/clean_manifest.c`.
   - Compile the fixed program to `/home/user/clean_manifest`.

4. **Create Final Manifest**: Run your compiled `/home/user/clean_manifest` tool, passing it your `/home/user/manifest.csv` via standard input. Redirect the output to `/home/user/final_manifest.csv`.

Ensure your final CSV precisely matches the requested format so that the automated verification system can parse it successfully.