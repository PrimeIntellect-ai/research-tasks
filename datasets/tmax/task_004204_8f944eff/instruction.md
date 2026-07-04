You are a storage administrator for a security company. The company records 24/7 surveillance footage, which consumes massive amounts of disk space. A significant portion of this footage is completely static (e.g., an empty hallway with no movement). 

Your objective is to build a storage-optimizing processing pipeline that deduplicates static video segments at the file-system level, without losing the ability to playback the continuous timeline.

We have provided a sample 60-second video at `/app/surveillance.mp4`.

Your task:
1. Write a Python script `/home/user/process_footage.py` that reads `/app/surveillance.mp4`.
2. Segment the video into exactly 1-second chunks (e.g., `chunk_00.mp4`, `chunk_01.mp4`, ..., `chunk_59.mp4`) and place them in `/home/user/archive/`.
3. Implement a change-detection algorithm in your script to analyze each chunk. Compare the frames within the chunk to determine if there is any significant motion.
4. **Deduplication via Hard Links:** For all chunks classified as "static" (no significant motion), keep only the *first* static chunk as a real file. For all subsequent static chunks, delete them and replace them with a **hard link** pointing to that first static chunk. This will significantly reduce disk space while maintaining the file structure for playback.
5. Chunks with motion must remain as independent, regular files.
6. Generate a log file at `/home/user/dedup_log.json` containing a dictionary mapping each chunk filename to a boolean indicating whether it was classified as motion (`true`) or static (`false`).

Requirements:
- You must use Python for the logic, though you can use `subprocess` to call `ffmpeg` for extraction.
- The system will evaluate your solution based on two metrics:
  a) **Fidelity:** The reconstructed video (concatenating `chunk_00.mp4` to `chunk_59.mp4`) must visually match the original video closely.
  b) **Storage Savings:** The physical disk space used by `/home/user/archive/` must be minimized through your hard-linking strategy.
- All file operations must be complete and the script must exit cleanly.

Run your script and ensure the final directory `/home/user/archive/` is populated correctly.