I am a researcher trying to organize a messy dataset from a recent physics experiment. The data pipeline crashed midway, leaving me with a raw video of the experiment and a heavily compressed, nested, and partially corrupted archive of sensor logs. 

I need you to write a Python-based data extraction pipeline that recovers the event timestamps from the sensor logs, extracts the corresponding frames from the video, and organizes them into a clean dataset structure.

Here are the details and your objectives:

1. **The Video**: The experiment recording is located at `/app/experiment.mp4`.
2. **The Sensor Archive**: Located at `/app/sensors.tar.gz`. 
   - This is a gzip-compressed tarball containing multiple zip files.
   - One of these zip files (you'll need to figure out which one by inspecting them) contains a binary file named `telemetry.bin`.
3. **Binary Parsing**: `telemetry.bin` has a custom binary format. 
   - The first 12 bytes are an ASCII header: `PHYS_EXP_V01`
   - The next 4 bytes represent an unsigned 32-bit integer (little-endian). This integer is the *byte offset* from the beginning of the file where the actual text-based event log starts.
   - Jump to that offset. From there to the end of the file is a block of messy text data.
4. **Text Transformation**: The text block contains mixed debug info and event triggers. You need to parse this text block (using Python, `awk`, `sed`, or a combination) to find lines that match the exact pattern: `[CRITICAL] EVENT_TRIGGERED at T=<timestamp>s`. 
   - Extract these timestamps (which are floating-point numbers in seconds).
5. **Frame Extraction & Organizing**: 
   - For every timestamp extracted, use `ffmpeg` (or an equivalent Python library) to extract the exact frame from `/app/experiment.mp4` at that timestamp.
   - Save the frames as JPEG images in `/app/dataset/frames/`, named as `frame_<timestamp>.jpg` (e.g., `frame_1.25.jpg`).
   - Finally, create a curated directory at `/app/dataset/curated/`. Inside this directory, create **symbolic links** to all frames where the timestamp is strictly greater than `10.0` seconds.

Write and execute the scripts necessary to automate this entire workflow. Do not just process the files manually; I need the Python script/pipeline that does this automatically, as I will run it on other similar datasets. Ensure your final extracted frames in `/app/dataset/frames/` are accurate.

Once your pipeline has completed, create a file called `/app/DONE` to indicate you are finished.