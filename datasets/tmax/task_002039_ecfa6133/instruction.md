I am migrating an old project off a legacy, proprietary version control system. This system used a custom checksum algorithm to track file changes and build manifests. I only have a stripped binary of the hasher tool left, located at `/app/manifest_hash_oracle`. 

I need your help to replace this binary and build a modern file watcher. Here are the requirements:

1. **Reverse Engineer the Hash**:
   Analyze `/app/manifest_hash_oracle`. It reads file content from standard input (`stdin`) until EOF and outputs a single 8-character hexadecimal string (the checksum) to standard output (`stdout`), followed by a newline. 
   Write a replacement tool at `/home/user/manifest_tool` (you can use Python, Node, C, or any language you prefer, but it must be executable via `./manifest_tool` or be a compiled binary at that exact path). It must process `stdin` and output the exact same hexadecimal hash as the oracle for any given input.

2. **Build a Watcher and Atomic Manifest Updater**:
   Write a script at `/home/user/watch_project.sh` that continuously watches the directory `/home/user/project/` for any file modifications or creations. 
   When a file changes, the script must:
   - Compute the custom hash of the changed file using your newly created `/home/user/manifest_tool`.
   - Update a central manifest file at `/home/user/manifest.txt`. The manifest format should be `<filename> <hash>` (one per line, where `<filename>` is the relative path from the project root).
   - Ensure that writes to `/home/user/manifest.txt` are strictly **atomic** (e.g., using temporary files and atomic `mv` operations) to prevent data corruption if the system crashes during an update. 

Please start by analyzing the oracle, writing your replacement hasher, and then creating the watcher script. Ensure `/home/user/manifest_tool` handles arbitrary binary input accurately.