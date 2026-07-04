I need help fixing and extending a configuration tracking script. 

I have a bash script at `/home/user/config_tracker.sh` that is supposed to read directory paths from `/home/user/watch_list.txt`, traverse them, and back up the files to `/home/user/archive/`. However, my script is currently getting stuck in an infinite loop because there is a symlink loop inside the `/home/user/monitored_data/` directory.

Please fix my script and add some missing functionality:
1. **Fix the infinite loop**: Modify the recursive directory traversal so that it completely ignores symlinks.
2. **File Chunking**: As the script copies files to `/home/user/archive/`, it must check the file size. 
   - If the file is 50KB or smaller, simply copy it to the archive with its original basename.
   - If the file is strictly larger than 50KB, split it into 50KB chunks inside the archive directory using the `split` command. The chunks should be named `[basename].part_aa`, `[basename].part_ab`, etc. (e.g., `largefile.bin.part_aa`).
3. **Manifest Generation**: The script must generate a manifest file at `/home/user/archive/manifest.txt`. For every file or chunk placed in the archive, append a line to the manifest in the exact following format:
   `[absolute path of the original file] | [archived file or chunk name] | [sha256 checksum of the archived file or chunk]`
   (Example: `/home/user/monitored_data/config.txt | config.txt | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`)
4. Ensure the manifest is sorted alphabetically by the absolute path of the original file, and then by the chunk name.

Finally, execute the script so that `/home/user/archive/` is fully populated and the `manifest.txt` is created. Do not change the files in `/home/user/monitored_data/` or the `watch_list.txt`.

The original broken script is provided in your environment.