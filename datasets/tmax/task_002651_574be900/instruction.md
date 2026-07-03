You are assisting a configuration manager in generating an update patch for a system's configuration files. The configurations consist of both small text files and large binary blobs. 

We need to identify which files have changed compared to a baseline manifest, generate a new manifest, and package the changes into an archive. Because some of our binary configs can be quite large in production, we have a strict requirement on how files are read.

Here is your task:
1. Look in the directory `/home/user/configs/`. It contains the current state of our configuration files.
2. Read the baseline manifest located at `/home/user/base_manifest.txt`. This file contains the SHA256 checksums of the files from the last deployment, in the format: `<sha256_hex> <filename>\n`.
3. Write a script (Python, Perl, or Ruby) to calculate the SHA256 checksum of every file currently in `/home/user/configs/`. 
   - **Crucial Requirement:** For any file larger than 1 MB (1,048,576 bytes), your script *must* use memory-mapped I/O (e.g., the `mmap` module in Python) to read the file contents for hashing. For smaller files, standard text/binary reading is fine.
4. Output a new manifest file to `/home/user/new_manifest.txt` containing the updated SHA256 checksums for all files currently in the directory, using the exact same format as the baseline manifest. Sort the lines alphabetically by filename.
5. Identify which files are new or have a different checksum compared to `base_manifest.txt`.
6. Create an uncompressed tar archive at `/home/user/config_patch.tar` containing *only* the modified and new files. The files inside the tar archive should not contain absolute paths (e.g., the archive should contain `web.json`, not `home/user/configs/web.json`).

Ensure your script handles binary and text reading appropriately. Leave the generated archive and the new manifest at the specified paths.