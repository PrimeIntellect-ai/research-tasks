You are an AI assistant helping a technical writer organize and compress a multimedia documentation package.

The writer has recorded a software demonstration, located at `/app/screen_demo.mp4`.
They also have a draft of their notes at `/home/user/docs/raw_notes.txt`, which contains timestamps corresponding to key events in the video.

Your task is to create a self-contained, highly compressed custom documentation archive by following these steps:

1. **Extract and Process Frames**: 
   Read `/home/user/docs/raw_notes.txt`. You will find several lines starting with a timestamp in the format `[MM:SS]`.
   For every timestamp found, extract the exact frame from `/app/screen_demo.mp4` at that time.
   To aggressively save space, you must convert these extracted frames to grayscale, resize them to exactly 320x240 pixels, and compress them as JPEGs. Save them as `frame_MM_SS.jpg` (e.g., `frame_00_15.jpg`).

2. **Bulk Edit Documentation**:
   Create a new file `/home/user/final_doc.md`. For each timestamp line in `raw_notes.txt`, replace the timestamp `[MM:SS]` with a Markdown image link to the corresponding frame: `![MM:SS](frame_MM_SS.jpg)`. Keep the rest of the text on that line intact.

3. **Custom Archiving**:
   The target system is an embedded documentation viewer that uses a custom binary archive format, not standard zip/tar. You must package `final_doc.md` and all the `frame_MM_SS.jpg` files into a single binary file located at `/home/user/doc_archive.pak`.

   The archive format must precisely follow this specification:
   - **Magic Header**: The first 8 bytes must be the ASCII string `DOCARCH1`.
   - **File Count**: The next 2 bytes must be an unsigned 16-bit integer (little-endian) representing the number of files in the archive.
   - **File Entries**: Immediately following the file count, for each file included:
     - **Filename Length**: 1 byte unsigned integer (length of the filename string).
     - **Filename**: The ASCII characters of the filename (e.g., `final_doc.md`). Do NOT include directory paths.
     - **File Size**: 4 bytes unsigned 32-bit integer (little-endian).
     - **File Data**: The raw bytes of the file.

4. **Optimization (Metric)**:
   The embedded system has extreme storage limits. The total size of `/home/user/doc_archive.pak` MUST be strictly less than 150,000 bytes. You will need to carefully tune your JPEG extraction/compression (e.g., lowering the JPEG quality setting) to ensure the final archive meets this threshold while keeping the images readable.

Make sure the final output strictly adheres to the custom binary format and size threshold.