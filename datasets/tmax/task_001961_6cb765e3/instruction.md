We are managing a large repository of binary artifacts and use a proprietary archiving format called `XAR2`. Our extraction tool, located at `/app/xar_tool`, is unfortunately vulnerable to various archive-based attacks (such as directory traversals, absolute path overwrites, and symlink loops that cause infinite loops during extraction or backup). 

The source code for `/app/xar_tool` has been lost, and it is a stripped binary. However, we know it creates and extracts `XAR2` archives.

Your task is to write a C++ sanitiser tool that reads a `XAR2` archive and determines if it is safe to extract. 

Requirements for the sanitiser:
1. It must be written in C++ and saved to `/home/user/sanitiser.cpp`. Compile it to `/home/user/sanitiser`.
2. It should take a single command-line argument: the path to a `.xar2` file.
3. It must exit with status `0` if the archive is perfectly safe, and exit with status `1` if it is malicious or malformed.
4. An archive is considered **malicious** if:
   - Any file, directory, or symlink path within the archive is an absolute path (starts with `/`).
   - Any path contains directory traversal components (`../`) that would resolve outside the root extraction directory.
   - Any symlink target is an absolute path or escapes the root extraction directory.
   - The archive contains a symlink loop or a symlink chain that exceeds a resolution depth of 5 steps.
5. You must reverse-engineer the `XAR2` binary format. You can use `/app/xar_tool` to create test archives to understand the format layout (e.g., headers, metadata, sizes). 

Two corpora of archives are provided for your testing:
- `/app/corpus/clean/`: Contains safe `.xar2` archives. Your tool must exit 0 for all of these.
- `/app/corpus/evil/`: Contains malicious `.xar2` archives designed to exploit the vulnerabilities. Your tool must exit 1 for all of these.

Your final executable must be located at `/home/user/sanitiser`.