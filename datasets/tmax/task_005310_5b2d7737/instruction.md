You are an artifact manager responsible for curating a repository of binary objects. A new batch of artifacts has been deposited in `/home/user/artifacts/`, but the repository is cluttered with old, irrelevant, or corrupted files.

Your task is to identify specific recently modified binary artifacts, extract their payloads using a custom C++ tool, and generate a final report.

Step 1: Write a C++ program
Create a C++ program at `/home/user/extractor.cpp` and compile it to `/home/user/extractor`.
This program must:
- Read raw binary data strictly from Standard Input (`stdin`).
- Check the first 4 bytes. They must perfectly match the ASCII string `ARTF` (the magic number).
- Read the next 4 bytes as an unsigned 32-bit integer (little-endian) representing the payload size `N`.
- Read exactly `N` bytes of payload data immediately following the size field.
- If the file is valid (has the correct magic number and at least `N` bytes of payload can be read), print the payload as an uppercase hexadecimal string (e.g., `4A4B4C`) to Standard Output (`stdout`), followed by a newline.
- If the magic number is incorrect, or if the stream ends before `N` bytes are read, print exactly the word `INVALID` to `stdout`, followed by a newline.

Step 2: Locate and process the artifacts
Using shell commands, find all files in the `/home/user/artifacts/` directory that meet ALL of the following metadata criteria:
- File extension is `.bin`
- File size is strictly greater than 15 bytes
- File was modified within the last 3 days (inclusive)

For each file found, use standard stream redirection to pipe its contents into your compiled `/home/user/extractor` program. 

Step 3: Generate the report
Create a text file at `/home/user/curation_report.txt` containing the results.
For each processed file, append a line in the exact following format:
`<full_absolute_path_to_file> - <output_from_extractor>`

Ensure the report is sorted alphabetically by the file path.