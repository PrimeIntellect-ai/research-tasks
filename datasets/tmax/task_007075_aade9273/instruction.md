You are an engineer tasked with building an artifact manager that curates binary repositories for a software organization. Developers upload randomly named compressed archives, and your system must watch for these uploads, inspect their contents on the fly, organize them into a structured repository, and manage "latest" release pointers.

Your task is to write, build, and run a Go program that satisfies the following requirements:

1. **Workspace Setup:**
   - Create your Go project in `/home/user/curator`.
   - The primary source file must be `/home/user/curator/main.go`.
   - You will manage two directories: `/home/user/incoming` (where artifacts are dropped) and `/home/user/repo` (where organized artifacts are stored). Create these directories.

2. **File Watching & Change Detection:**
   - Your Go program must use `github.com/fsnotify/fsnotify` to watch the `/home/user/incoming` directory for new file creation events.
   - If a file named exactly `SHUTDOWN.txt` is created in `/home/user/incoming`, the program must gracefully terminate with exit code 0.

3. **Compressed Stream Processing:**
   - When a `.tar.gz` file is detected in the `incoming` directory, your program must open it and read its contents without fully extracting it to disk.
   - Scan the archive for a file named exactly `manifest.txt`. 
   - Parse this text file to extract the application name and version. The file will strictly contain two lines:
     `AppName: <name>`
     `Version: <version>`

4. **Bulk File Renaming & Moving:**
   - Once the application name and version are extracted, move the original `.tar.gz` file from `/home/user/incoming` into the repository under the following structure:
     `/home/user/repo/<AppName>/<AppName>-<Version>.tar.gz`
   - You must create the `<AppName>` directory if it does not exist.

5. **Symbolic Link Management:**
   - After moving the file, create or update a symbolic link at `/home/user/repo/<AppName>/latest.tar.gz` that points directly to the newly moved `<AppName>-<Version>.tar.gz` file in the same directory.
   - Note: The symlink should use a relative target (e.g., `frontend-1.0.0.tar.gz`, not the absolute path) so the repository remains portable.

6. **Execution:**
   - Compile your program to an executable named `/home/user/curator/curator`.
   - Start your program in the background (e.g., `./curator &`).
   - Once the program is successfully running and actively watching the directory, create a file at `/home/user/curator/status.txt` containing the word `READY`. 

*Note: Do not leave `.tar.gz` files in the `incoming` directory once they are processed. The automated test will verify your implementation by looking for `status.txt`, dropping new test `.tar.gz` archives into `incoming`, and subsequently dropping `SHUTDOWN.txt` before verifying the final state of the `repo` directory.*