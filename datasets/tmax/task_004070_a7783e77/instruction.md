You are assisting a researcher who is organizing a large multimodal dataset on a Linux system. The researcher has run into issues with broken backup scripts crashing due to symbolic link infinite loops created by automated dataset tools. 

Your task consists of two parts: processing a video dataset, and building an adversarial filter for the backup system.

**Part 1: Video Processing**
You are provided with a video artifact of a lab experiment located at `/app/experiment.mp4`.
Using standard command-line tools (e.g., `ffmpeg`), extract frames from this video at a rate of 1 frame per second. 
Save these frames into `/home/user/dataset/frames/` using the naming convention `frame_XXXX.jpg` (starting at `frame_0001.jpg`).

**Part 2: Backup Filter Implementation**
The researcher wants to incrementally backup their datasets but the backup system keeps freezing because some dataset directories contain symbolic links that form infinite loops or escape the dataset root. 

You must write a script at `/home/user/backup_filter.py` (or a bash script `/home/user/backup_filter.sh`) that acts as a sanitizer for the backup system.
Your script should:
1. Accept a single directory path as a command-line argument.
2. Traverse the directory recursively.
3. Print the absolute paths of all safe files, directories, and symlinks to standard output (one per line).
4. **Omit (filter out)** any symbolic links that form an infinite loop (cyclic links).
5. **Omit (filter out)** any symbolic links that resolve to a path entirely outside the provided base directory (path escapes).

To ensure your script is robust, we have provided two test corpora:
- `/app/corpora/clean/`: Contains valid data structures, files, and safe internal symlinks. Your script must output all elements in this directory.
- `/app/corpora/evil/`: Contains malicious or corrupted dataset structures, including deep cyclic symlink loops and out-of-bounds references. Your script must successfully traverse the directory without hanging, and omit the dangerous links.

Ensure your filter script is executable and robust enough to handle the provided corpora before finishing.