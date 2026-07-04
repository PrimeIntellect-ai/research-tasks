You are an AI assistant helping a data researcher automate their incoming dataset pipeline. The researcher receives continuous streams of batched data in the form of nested archives and needs a reliable, automated way to unpack and organize them without corrupting the state if the system crashes during an update.

Your task is to write a C++ program that acts as a file watcher and organizer. 

Here are the complete specifications:

1. **Environment Setup:**
   - Create two directories: `/home/user/incoming` and `/home/user/dataset_links`.

2. **The C++ Watcher (`/home/user/organizer.cpp`):**
   - Write a C++ program and compile it to `/home/user/organizer`.
   - The program must use Linux `inotify` to continuously watch the `/home/user/incoming` directory for new files (specifically listening for `IN_CLOSE_WRITE` or `IN_MOVED_TO` events).
   - When a new file matching the pattern `*.zip` appears, the program must process it.

3. **Archive Processing (Nested Archives):**
   - The `.zip` files contain a directory structure that eventually holds `.tar.gz` files.
   - The program must extract the `.zip` file into a dynamically created temporary directory.
   - It must recursively find all `.tar.gz` files within the extracted content and extract them as well.
   - Finally, it must locate all `.csv` files that were unpacked from these nested archives. (You may use standard `system()` calls to `unzip`, `tar`, and `find` if you wish, or use C++ libraries).

4. **Symlink Management:**
   - For every `.csv` file found, create a symbolic link in `/home/user/dataset_links/` pointing to the absolute path of the extracted `.csv` file in the temporary directory. 
   - The symlink should have the same name as the `.csv` file.

5. **Atomic Manifest Update:**
   - The program must maintain a manifest file at `/home/user/dataset_links/manifest.log`.
   - The manifest file must contain the base filenames of all successfully symlinked `.csv` files so far, one per line, sorted alphabetically.
   - **CRITICAL:** The update to `manifest.log` must be strictly atomic. You must write the updated list to a temporary file (e.g., `/home/user/dataset_links/manifest.log.tmp`) and use the POSIX `rename()` function to replace the original file. Direct appending or standard overwriting is not allowed.

6. **Execution:**
   - Compile your program using standard `g++`.
   - Write a bash script `/home/user/start.sh` that compiles the C++ program (if not already compiled) and runs it in the background.

The automated verification will run `/home/user/start.sh`, drop a complex nested `.zip` into `/home/user/incoming`, wait a few seconds, and then verify the atomic creation of the manifest and the correctness of the symlinks.