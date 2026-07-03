You are tasked with fixing a custom configuration backup tool written in C, and then using it to perform an incremental tracking operation on a Linux filesystem. 

In `/home/user/workspace/` you will find a C program named `tracker.c`. This program is designed to recursively traverse a directory, follow symbolic links, and record the state (size and modification time) of all regular files into a snapshot text file. The snapshot format is: `<absolute_path> <size> <mtime>`.

However, the configuration directory it needs to track, `/home/user/config_root/`, contains a symlink loop. Because `tracker.c` blindly follows symlinks, running it currently results in an infinite loop and eventually a stack overflow or path length limit error.

Your objectives:
1. **Fix the C program**: Modify `/home/user/workspace/tracker.c` so that it safely follows directory symlinks but prevents infinite loops. You must do this by tracking the `dev_t` and `ino_t` (device and inode numbers) of directories as you visit them. If a directory has already been visited, skip it.
2. **Compile**: Compile the fixed program to `/home/user/workspace/tracker`.
3. **Initial Snapshot**: Run `./tracker /home/user/config_root/ /home/user/workspace/snapshot1.txt` to create the baseline snapshot.
4. **Simulate Configuration Changes**: 
   - Append the line `DEBUG=true` to the file `/home/user/config_root/app2/settings.conf`.
   - Create a new file `/home/user/config_root/app1/new_config.txt` containing the text `version=2`.
5. **Secondary Snapshot**: Run the tracker again to produce `/home/user/workspace/snapshot2.txt`.
6. **Differential Report**: Create a file named `/home/user/diff_report.txt` that lists the absolute paths of all files that were added or modified between `snapshot1.txt` and `snapshot2.txt`. The paths must be listed one per line, sorted alphabetically. You can use any shell utilities (like `comm`, `awk`, `diff`) or write another C program to generate this report.

Ensure that your fixed `tracker.c` program compiles without errors and successfully handles the symlink loop without skipping valid, unvisited directories.