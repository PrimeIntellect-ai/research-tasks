You are a storage administrator managing a highly constrained edge server. We have a surveillance video taking up too much space, and we need to archive its frames efficiently. Because the camera is mostly static, many adjacent frames are identical or near-identical, making standard archiving less optimal than a custom deduplication approach.

Your task is to implement an end-to-end archiving workflow:

1. **Frame Extraction**: Extract all frames from the video `/app/surveillance.mp4` as PNG images into `/home/user/raw_frames/`. They should initially be named `out_0001.png`, `out_0002.png`, etc. (using 1-based indexing).
2. **Bulk Renaming**: Bulk rename all extracted frames in `/home/user/raw_frames/` so they follow the pattern `cam_A_frame_<N>.png`, where `<N>` is the 4-digit zero-padded frame number (e.g., `cam_A_frame_0001.png`).
3. **Custom Deduplicating Archiver (C Language)**: 
   Write a C program named `/home/user/archiver.c` and compile it to `/home/user/archiver`. This program must implement a custom binary archive format that deduplicates identical files.
   The program must accept the following command-line arguments:
   - `./archiver pack <input_directory> <archive_file>`: Reads all `.png` files in the input directory, identifies exact duplicates (files with identical byte content), stores the unique file data only once in the archive, and writes the required metadata (filenames and pointers to the data blocks) to reconstruct the directory.
   - `./archiver unpack <archive_file> <output_directory>`: Extracts the files from the archive, correctly reconstructing all files (including duplicates) with their original filenames.
   - `./archiver verify <archive_file>`: Verifies the integrity of the archive without writing files to disk (e.g., checking internal headers, checksums, or structural consistency). Returns exit code 0 if valid, non-zero otherwise.

4. **Execution**: Run your compiled program to pack `/home/user/raw_frames/` into `/home/user/surveillance.dedup`. 

To succeed, your deduplicating archiver must correctly reconstruct the original files, and the resulting `/home/user/surveillance.dedup` must achieve a compression ratio (Archive Size / Total Original PNG Size) strictly less than 0.25 (since the video contains mostly static frames).