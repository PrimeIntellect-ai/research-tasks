You are assisting a technical writer who manages a large set of documentation. The writer frequently creates snapshots (releases) of the documentation drafts. Because binary assets (like images) are large and rarely change, but markdown text files change often, they need an efficient publishing script. Also, since this script might be triggered simultaneously by different continuous integration pipelines, it must be concurrency-safe.

Your task is to write a Bash script named `/home/user/publish.sh` that securely and efficiently publishes the current draft documentation into a release folder. 

Here are the exact requirements for `/home/user/publish.sh`:

1. **Arguments:** The script must accept exactly one argument: the release name (e.g., `v1.0`).
2. **Concurrency (File Locking):** The entire publishing process must be protected by an exclusive file lock using `flock` on the file `/home/user/releases/.lock`. If another instance is running, the script should wait for the lock.
3. **Paths:** 
   - Source drafts are located in `/home/user/docs_draft/`.
   - Releases should be stored in `/home/user/releases/<release_name>/`.
4. **Text Transformation (Text File Read/Write):** 
   - Iterate through all `.md` files in `/home/user/docs_draft/`.
   - Copy each `.md` file to the new release directory.
   - Append a new line containing exactly the text `Status: PUBLISHED` to the end of each copied `.md` file in the release directory.
5. **Incremental Backup (Hard Linking Binaries):**
   - Iterate through all `.png` files in `/home/user/docs_draft/`.
   - If a directory exists at `/home/user/releases/latest`, check if the `.png` file exists inside it.
   - If it exists in the `latest` release, create a **hard link** of that `.png` file from the `latest` release into the new `<release_name>` directory (to save disk space).
   - If it does NOT exist in the `latest` release, perform a standard copy of the `.png` from `docs_draft` to the new release directory.
6. **Symlink Management:**
   - After successfully processing all files, update a symbolic link at `/home/user/releases/latest` so that it points to the newly created release directory (e.g., `/home/user/releases/<release_name>`). The symlink must be a relative or absolute path that correctly resolves to the new release folder.

**Setup and Execution Instructions:**
1. The `/home/user/docs_draft/` directory and some initial files already exist.
2. Create the `publish.sh` script and make it executable.
3. Run your script to create the first release: `./publish.sh v1.0`
4. Create a new dummy image file in drafts: `echo "fake image data" > /home/user/docs_draft/img2.png`
5. Modify `doc1.md` in drafts: `echo "Extra line" >> /home/user/docs_draft/doc1.md`
6. Run your script again to create a second release: `./publish.sh v1.1`

By the end of this task, `/home/user/releases/v1.0/` and `/home/user/releases/v1.1/` must exist with the correct files, transformations, hard links, and the `latest` symlink correctly pointing to `v1.1`.