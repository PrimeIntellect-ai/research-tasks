I am a researcher organizing a massive dataset of high-speed video recordings, and I need help creating a custom archiving script. 

We have a sample video located at `/app/experiment_record.mp4`. I need you to write a Python script `/home/user/archive_video.py` that does the following:
1. Uses `ffmpeg` (which is pre-installed) to extract the first 5 seconds of the video, split into 1-second chunks (at 10 frames per second).
2. Converts the frames of each 1-second chunk into grayscale raw bytes.
3. Implements a custom delta-encoding compression across the frames within each chunk. Specifically, the first frame of a chunk is stored as raw bytes, and subsequent frames in that chunk are stored as the byte-wise difference from the previous frame. Run-Length Encoding (RLE) should then be applied to the flattened differences.
4. Appends each compressed chunk to a single binary archive file `/home/user/dataset.archive`. You must implement file locking (`fcntl`) when writing to this file, simulating a scenario where multiple concurrent jobs are writing to the same archive.
5. Generates a manifest file `/home/user/manifest.json` containing the SHA256 checksums of the uncompressed raw byte payload for each of the 5 chunks, their byte offsets in the `dataset.archive`, and their compressed sizes.

To succeed, your delta+RLE compression must be effective enough to reduce the total archive size. The automated system will test your archive to ensure it is perfectly lossless (MSE = 0 compared to the original grayscale frames) and that the final `dataset.archive` size is less than 65% of the uncompressed raw frame size.