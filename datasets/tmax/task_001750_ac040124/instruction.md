You are acting as an assistant to a technical writer who is organizing documentation for a recent software release. The writer has a video recording of a software demo and a legacy archive of old documentation that needs to be updated, re-encoded, and packaged.

Your task involves the following steps:

1. **Video Frame Extraction**: There is a video recording located at `/app/demo_recording.mp4`. You need to extract exactly 5 frames from this video at the following timestamps: `00:00:02`, `00:00:04`, `00:00:06`, `00:00:08`, and `00:00:10`. Save these frames as `frame_2.jpg`, `frame_4.jpg`, `frame_6.jpg`, `frame_8.jpg`, and `frame_10.jpg`. Ensure high quality extraction.

2. **Archive Extraction and Integrity**: There is an archive at `/app/legacy_docs.tar.gz`. First, verify its integrity. Extract its contents.

3. **Text Transformation and Encoding**: The extracted text files (`.txt`) are currently encoded in `ISO-8859-1`. You must:
   - Convert all `.txt` files to `UTF-8` character encoding.
   - Using `sed`, `awk`, or a custom script (using memory-mapped I/O if the files are large), replace all instances of the string `AcmeCorp` with `NovaTech` in every text file.

4. **Final Packaging**: Create a new archive named `/home/user/docs_package.tar.gz` containing:
   - The 5 extracted `frame_*.jpg` files.
   - The converted and updated `.txt` files.
   Do not include any intermediate directories unless they were present in the original archive.

Your success will be evaluated based on the accurate replacement of the text, the correct encoding of the files, and a numerical metric: the average Structural Similarity Index Measure (SSIM) of your extracted frames compared to a ground-truth set of frames. Your average SSIM must be >= 0.95.