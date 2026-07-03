You are assisting a researcher who is organizing a large video dataset. The researcher needs a highly efficient tool to extract raw frames from video files, compress them on-the-fly, chunk the data to mimic log rotation, and generate structured metadata. 

There is a test video located at `/app/video.mp4`. 

Your objective is to write a C program that performs the following multi-stage workflow:

1. **Video Ingestion:** Your C program should read raw grayscale (8-bit) video frames from standard input. You will run `ffmpeg` to decode `/app/video.mp4` to raw grayscale at 10 fps, and pipe the output to your C program.
2. **Chunking & Compression:** As your C program reads the raw frames stream, it must compress the data using `zlib` (e.g., using `gzopen`, `gzwrite`) and split it into multiple chunk files in the `/home/user/chunks/` directory. 
    * A new chunk file (named `chunk_000.gz`, `chunk_001.gz`, etc.) must be started exactly every 30 frames.
3. **Symlink Management:** While writing each chunk, maintain a symbolic link at `/home/user/chunks/latest.gz` that always points to the chunk currently being written or most recently completed.
4. **Structured Parsing & Encoding:** Once processing is complete, your program (or a subsequent script you write) must generate a CSV index of the chunks at `/home/user/chunks/index.csv`. The CSV must have the header `chunk_name,num_frames,compressed_bytes`. Finally, convert this `index.csv` file from UTF-8 to UTF-16LE encoding, saving it as `/home/user/chunks/index_utf16.csv`.

**Constraints:**
* Use **C** as the primary language for the ingestion, chunking, and compression logic. You may use shell commands to invoke `ffmpeg`, handle the encoding conversion (e.g., `iconv`), and pipeline everything.
* To achieve the required metric, you must maximize compression efficiency. Configure zlib to use the maximum compression level (level 9). 

Your final evaluation will be based on the validity of the UTF-16LE CSV file, the integrity of the gzip chunks, and a **metric threshold** evaluating the total compressed file size of the chunks to ensure maximum compression was used.