You are helping a technical writer organize a set of documentation files that were accidentally extracted all over the home directory due to a poorly formatted archive. 

You need to reassemble the documentation into coherent manuals. Here is what you need to do:

1. **Interpret the Configuration**: There is a configuration file located at `/home/user/doc_build.conf`. It is an INI-style file. Each section represents a manual. The `chunks` key contains a comma-separated list of filenames that make up the manual, in the correct order. The `output` key specifies the absolute path where the final merged markdown file should be saved.
2. **Locate the Chunks**: Because the archive extraction was flawed, the chunk files (e.g., `.txt` files) are scattered somewhere inside `/home/user/` or its subdirectories. You must find the exact locations of these specific chunk files. All valid chunk files were created recently and are regular files.
3. **Format and Merge**: For each manual, read the corresponding chunk files in the exact order specified in the `chunks` list. Before appending a chunk's content to the final merged file, you must apply the following text replacements to fix the formatting:
   - Replace the exact string `[[H1]] ` (including the space) with `# `
   - Replace the exact string `[[H2]] ` (including the space) with `## `
   Merge the formatted chunks and save the result to the path specified in the `output` key of the configuration file. Ensure the destination directories exist. Add a single newline character between the contents of each chunk.
4. **Link Management**:
   - Create a directory called `/home/user/publish/`.
   - Create hard links for all the successfully generated final markdown files into the `/home/user/publish/` directory. Keep the same filenames.
   - Create a symbolic link at `/home/user/latest_docs` that points to the `/home/user/publish/` directory.

Use any programming language or shell script you prefer to automate this process. Make sure the final files and links are correctly placed.