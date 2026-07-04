You are an AI assistant helping a technical writer organize and archive an old documentation repository.

The technical writer has a collection of raw documentation files located in `/home/user/docs_raw/`. These files are a mix of `.md` and `.txt` files. They contain outdated copyright notices and need to be packaged into a single, highly specific custom archive format for a legacy document management system.

Your task is to write a Bash script at `/home/user/pack_docs.sh` that performs the following steps:
1. Creates the output directory `/home/user/archive/` if it doesn't exist.
2. Finds all `.md` and `.txt` files in `/home/user/docs_raw/` (including subdirectories) and processes them sorted alphabetically by their full file path.
3. Streams the files into a single pipeline that applies the following transformations:
   - For every file, injects a custom header line exactly formatted as `===FILE: <basename>===` immediately before the file's content (where `<basename>` is the name of the file without the directory path).
   - Replaces all instances of the exact string "Copyright 2018 Acme Corp" with "Copyright 2024 Acme Global" using stream processing (`sed` or `awk`).
   - Appends a newline after each file's content if it doesn't already end with one, ensuring the next header starts on a new line.
4. Compresses this combined, transformed text stream using `gzip`.
5. Writes the final compressed output to `/home/user/archive/docs_custom.gz`.

The script must be executable. Run the script once you have written it so the archive is generated.

Do not use temporary files for the transformed text; everything must be streamed directly into the gzip process to handle potentially massive document sets efficiently.