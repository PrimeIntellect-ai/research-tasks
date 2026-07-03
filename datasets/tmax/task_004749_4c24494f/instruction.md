You are an AI assistant helping a technical writer organize and modernize a legacy documentation archive.

The legacy documentation is stored in a tar archive at `/home/user/docs_project/old_manuals.tar`. 
Inside this uncompressed tarball, there are several individual gzip-compressed text files (e.g., `chapter1.txt.gz`, `chapter2.txt.gz`). 

These files have three major legacy issues:
1. They are encoded in `ISO-8859-1`, but we need them in `UTF-8`.
2. They use a legacy custom markup for headers: `<<TITLE>>Some Title<</TITLE>>`. This needs to be converted to standard Markdown H1 headers: `# Some Title`.
3. They need to be converted to Markdown files (`.md.gz`).

Your task is to automate this transformation. 

**Requirements:**
1. **Dependency Installation:** You will need to install any necessary C development libraries (like `zlib1g-dev`) and tools to complete the task.
2. **C Program (`transformer.c`):** Write a C program at `/home/user/docs_project/transformer.c` that does the heavy lifting. The program must:
   - Accept two command-line arguments: an input `.txt.gz` file path and an output `.md.gz` file path.
   - Use the `zlib` library to directly read the compressed input stream and write to the compressed output stream.
   - Convert the character encoding of the text stream from `ISO-8859-1` to `UTF-8`.
   - Perform the format conversion, replacing any instances of `<<TITLE>>` with `# ` (and removing the closing `<</TITLE>>`).
3. **Shell Script (`process.sh`):** Write a bash script at `/home/user/docs_project/process.sh` that:
   - Compiles your C program.
   - Extracts the `old_manuals.tar` archive.
   - Iterates over all extracted `.txt.gz` files and processes them using your compiled C program to produce corresponding `.md.gz` files.
   - Creates a final zip archive named `/home/user/docs_project/modern_manuals.zip` containing ONLY the newly generated `.md.gz` files.

**Final State:**
When you are finished, the script `process.sh` must have been executed successfully, leaving the `modern_manuals.zip` file in `/home/user/docs_project/`. The zip file should contain the correctly converted, UTF-8 encoded, and zlib-compressed markdown files.