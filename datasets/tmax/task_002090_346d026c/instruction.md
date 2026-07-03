You are helping a technical writer recover a corrupted documentation backup. The backup was steganographically encoded into a video file during a glitchy automated archival process.

You have been provided with a video file at `/app/docs_walkthrough.mp4`. 

Here is your workflow to recover the documentation:

1. **Extract Frames:** Extract the frames of `/app/docs_walkthrough.mp4` at 1 frame per second as raw grayscale images (e.g., `.pgm` or `.raw` format) using `ffmpeg`.
2. **C Extraction Program:** Write a C program named `/home/user/extractor.c` that reads the extracted image files in alphabetical order. The original backup archive was hidden in the Least Significant Bit (LSB) of each pixel's grayscale value. 
    * Extract the lowest bit of each pixel byte.
    * Pack these bits into bytes (8 pixels = 1 byte, MSB first).
    * Write the resulting binary stream to `/home/user/recovered.tar`. The stream may contain trailing garbage bytes after the EOF of the tar file; `tar` will typically ignore this, but ensure the file is written correctly.
3. **Archive Extraction & Cleanup:** Extract `/home/user/recovered.tar` into a new directory `/home/user/docs_raw`. 
    * The archive is known to contain a messy structure with **infinite symlink loops** (created by a malfunctioning backup script). Identify and delete any symlinks that point back to their own parent directories to break the loops.
    * There are nested multi-part archives (e.g., `assets.tar.gz`) inside. Extract them in their respective subdirectories and delete the archive files.
    * All documentation text files (`.txt`) were saved in `ISO-8859-1` encoding. Convert all `.txt` files in the cleaned directory tree to `UTF-8`.
4. **Final Packaging:** Once the directory is cleaned, symlink loops are removed, nested archives are expanded, and encodings are fixed, compress the entire `/home/user/docs_raw` directory into `/home/user/clean_docs.tar.gz`.

Ensure your C code is compiled efficiently (e.g., `gcc -O2`) to process the frames within a reasonable time limit. The final output must be exactly at `/home/user/clean_docs.tar.gz`.