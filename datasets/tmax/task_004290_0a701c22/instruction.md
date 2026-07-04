You are a storage administrator tasked with recovering disk space and analyzing an incident caused by a rogue backup script. The script created infinite symlink loops, duplicated massive amounts of data, and nearly crashed the server.

You need to perform the following operations:

1. **Video Log Analysis**: 
   A system monitoring tool recorded the disk IO status LED during the incident, saved at `/app/disk_monitor.mp4`. The video is 30 FPS. In this video, the top-left 10x10 pixel region acts as an "alert LED." When the disk IO was critically blocked, this LED turned bright red (RGB values approximately R>200, G<50, B<50). 
   Use `ffmpeg` and any scripting language (Python, Perl, etc.) to extract the frames, analyze the pixels, and count the total number of frames where the alert LED was red. Write this integer to `/home/user/alert_frames.txt`.

2. **Nested Archive Extraction & Parsing**:
   The rogue script's logs were aggressively compressed into a nested archive at `/home/user/backups/incident_logs.tar.gz`. 
   Extract this archive (it contains a `.zip` file, which in turn contains `.tar.bz2`, which finally contains `error.log`). 
   Parse `error.log` using text transformation tools (like `sed`, `awk`, or a script) to extract all unique file paths following the exact string `ELOOP: Too many levels of symbolic links: `.

3. **Symlink Cleanup & File Deduplication**:
   The extracted paths from step 2 point to symlink loops inside `/home/user/data/`. Delete every symlink that caused an ELOOP error.
   Next, you will find many regular files in `/home/user/data/` that are exact duplicates of one another. To save space, find all duplicate regular files and replace them with hardlinks to a single copy of the file.

4. **Final Archiving**:
   Once the symlinks are removed and duplicates are hardlinked, create a compressed gzip tarball of the entire `/home/user/data/` directory at `/home/user/optimized_data.tar.gz`.

Provide the commands and scripts you use. The automated system will evaluate your success based on the accuracy of your frame count and the final byte size of your `optimized_data.tar.gz` archive.