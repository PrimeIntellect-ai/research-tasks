You are acting as an automated assistant for a technical writer who is organizing a large batch of newly received documentation. 

You have been provided with an archive located at `/home/user/incoming_docs.tar.gz`. 
Your task is to extract this archive, verify the integrity of the documentation files based on a configuration manifest, and generate a markdown index file using a custom C++ program.

Please follow these exact steps:
1. Extract `/home/user/incoming_docs.tar.gz` into the directory `/home/user/extracted_docs/`.
2. Inside the extracted directory, you will find a configuration file named `doc_map.ini`. The file contains a `[Docs]` section, followed by key-value pairs representing the documentation files. The format of each line under `[Docs]` is:
   `key=relative/path/to/file|expected_size_in_bytes`
3. Write a C++ program at `/home/user/parser.cpp` and compile it. The program must:
   - Parse `doc_map.ini`.
   - Verify the "integrity" of each file listed. A file is considered valid *only* if it exists at the specified relative path (relative to `/home/user/extracted_docs/`) AND its actual file size exactly matches the `expected_size_in_bytes`. Ignore any files that are missing or have a size mismatch.
   - Filter the valid files to include *only* text documents (files whose paths end in `.txt`).
   - Open each valid `.txt` document and read exactly the first line of the file. This first line is considered the document's "Title".
   - Generate an output markdown file at `/home/user/doc_index.md`.
4. The generated `/home/user/doc_index.md` must contain a bulleted list of the valid text files and their titles, formatted exactly as follows:
   `- {relative/path/to/file}: {Title}`
   The list must be sorted alphabetically by the relative file path.

Example output format for `/home/user/doc_index.md`:
`- docs/api/auth.txt: Authentication API Overview`
`- docs/intro.txt: Welcome to the Documentation`

Ensure your C++ code is robust enough to handle basic file operations, string parsing, and file size verification using standard C++ libraries. Run your compiled program to generate the final `doc_index.md` file.