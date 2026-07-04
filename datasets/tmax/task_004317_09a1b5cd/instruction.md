You are acting as a backup administrator who needs to build a reactive archiving tool.

Your task is to create a Go program that watches a directory tree for any changes and automatically creates a compressed backup snapshot when a change occurs. 

Please perform the following steps:
1. Initialize a Go module named `auto_archiver` in `/home/user/archiver` and download the `github.com/fsnotify/fsnotify` package.
2. Write a Go program at `/home/user/archiver/main.go` that:
   - Takes a single command-line argument: the absolute path of a directory to watch.
   - Recursively traverses the given directory and adds the directory and all of its subdirectories to an `fsnotify` watcher.
   - Blocks and waits for any file `Create` or `Write` event within those watched directories.
   - Upon detecting the *first* such event, creates a `.tar.gz` archive of the entire watched directory tree. The archive must be saved to `/home/user/snapshot.tar.gz`.
   - Writes the absolute path of the specific file that triggered the event to `/home/user/trigger.log`.
   - Exits cleanly with status code 0 immediately after creating the archive and log file.
3. Prepare the testing environment by creating a directory structure `/home/user/workdir/subdir` and placing a dummy file `/home/user/workdir/initial.txt` with the content "INIT" inside it.
4. Build and run your Go program in the background, instructing it to watch `/home/user/workdir`.
5. Trigger the backup by creating a new file at `/home/user/workdir/subdir/trigger.txt` containing the text "BACKUP_ME".
6. Wait for your program to create `/home/user/snapshot.tar.gz` and `/home/user/trigger.log`, and ensure the program has exited.

Requirements for the `.tar.gz`:
- The archive should store files relative to the watched directory. For example, the trigger file should be inside the archive as `subdir/trigger.txt` (or similar relative path structure), not under the full absolute path `/home/user/workdir/...`.