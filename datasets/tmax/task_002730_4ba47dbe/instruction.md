You are acting as a storage administrator responding to an extraction incident. An automated archival process ran amok, resulting in a "zip slip" vulnerability that dropped files and malicious symlinks outside the intended directory, while also creating thousands of duplicate files that are exhausting our disk space. 

We captured a screencast of the terminal when the incident occurred, located at `/app/extraction_incident.mp4`. 

Your objectives are:
1. **Identify the Target**: Analyze the video `/app/extraction_incident.mp4` (ffmpeg is installed) to find the specific "TARGET_DIR" path that was infected. The path is displayed in the video.
2. **Remediate Symlinks**: Write a Rust program that traverses this target directory. Any symbolic link that points *outside* of the target directory must be deleted and replaced with a regular text file containing exactly the string `INVALID_LINK_REMOVED`. 
3. **Deduplicate via Hard Links**: The extraction dumped thousands of identical log files. Your Rust program must use streaming or memory-mapped I/O to efficiently read the files, identify duplicates by their content, and replace identical files with hard links to a single physical file, drastically reducing disk space.
4. **Compile and Execute**: Compile your Rust program (use `cargo init` or `rustc` directly) and run it against the target directory.

**Constraints:**
- You must use **Rust** for the directory traversal, symlink remediation, and deduplication logic.
- The deduplication must rely on creating hard links.

Your final success will be evaluated by a metric threshold: the total disk usage of the target directory (in bytes) must be strictly reduced below a specific target due to successful hard-linking, and zero malicious symlinks must remain.