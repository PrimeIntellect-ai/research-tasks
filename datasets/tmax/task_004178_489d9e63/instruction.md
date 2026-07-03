We are currently organizing and migrating a massive folder of legacy project files located at `/home/user/legacy_project/`. These files contain custom binary headers that dictate how they should be processed. 

Historically, we used a proprietary utility to read these headers. We have a recovered copy of this utility at `/app/legacy_indexer`, but it is a stripped binary, heavily outdated, and fails to integrate with our modern CI pipeline. 

Your task is to completely replace this utility by reverse-engineering its behavior and writing a drop-in replacement, and then applying it to the project repository.

Here are your specific objectives:

1. **Reverse Engineer the Header Format:** 
   Analyze the behavior of `/app/legacy_indexer`. It takes a single file path as an argument. By passing it various test files, deduce exactly how it reads the binary header, extracts the metadata, and formats its standard output (and standard error / exit codes for invalid files). 

2. **Develop a Replacement:**
   Write your own script or program at `/home/user/my_indexer`. You may use any language or standard Linux utilities (e.g., bash, awk, python, perl). 
   - It must take a single file path as an argument: `/home/user/my_indexer <path_to_file>`
   - It must produce *bit-exact equivalent* output (stdout and stderr) and exit codes as `/app/legacy_indexer` for ANY given file.
   - It must gracefully handle files of any size without crashing, reading only the necessary header bytes.

3. **Traverse and Organize:**
   Recursively traverse all files in `/home/user/legacy_project/`. For every file, use your new `/home/user/my_indexer` to extract the metadata. 
   - If the file has a valid header, format the output using `sed` or `awk` to prefix the line with the file's relative path (e.g., `./assets/sprite.dat: [METADATA_STRING]`).
   - Use atomic writes to safely append these valid entries to a final manifest file at `/home/user/project_manifest.txt`.

Our automated CI test will forcefully fuzz `/home/user/my_indexer` against `/app/legacy_indexer` with thousands of randomized binary inputs to ensure strict equivalence before deploying your tool.