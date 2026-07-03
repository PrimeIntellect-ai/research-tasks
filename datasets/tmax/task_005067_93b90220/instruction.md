You are an ML engineer preparing a multimodal training dataset from a raw video file. To minimize storage and focus the model on the primary subject, we need to extract raw frames, crop them, calculate average color intensities, and tokenize the results into a compact binary format.

We have a source video located at `/app/training_source.mp4`.

Your task is to build a high-performance ETL pipeline. You must write a Go program that acts as our "Video Tokenizer".

**Step 1: Write the Video Tokenizer in Go**
Create a Go program at `/home/user/video_tokenizer.go` and compile it to `/home/user/video_tokenizer`.
The program should read raw `rgb24` video frame data from standard input (`stdin`) and write tokenized binary data to standard output (`stdout`).
- Assume the input video resolution is exactly 320x240 pixels (Width x Height).
- A single frame consists of `320 * 240 * 3` bytes (R, G, B values for each pixel, row by row from top to bottom, left to right).
- For each complete frame received, consider ONLY the center 160x120 region (i.e., skipping 80 pixels from the left/right and 60 pixels from the top/bottom).
- Calculate the integer average (using integer division truncating towards zero) of the Red, Green, and Blue channels independently over this 160x120 region.
- Compute a 16-bit token for the frame using this bitwise formula:
  `Token = (avgR >> 4) << 8 | (avgG >> 4) << 4 | (avgB >> 4)`
- Write this token as a 16-bit integer in **little-endian** byte order to `stdout`.
- Process as many complete frames as are available in `stdin`. Discard any trailing partial frame bytes.

**Step 2: Construct the ETL Pipeline**
Create a shell script at `/home/user/run_pipeline.sh` that performs the end-to-end dataset preparation:
1. Use `ffmpeg` to read `/app/training_source.mp4`.
2. Extract frames at a rate of 5 frames per second.
3. Resize the output to 320x240 (if not already).
4. Output in raw `rgb24` format to standard output.
5. Pipe the output into your `/home/user/video_tokenizer` binary.
6. Redirect the final token stream to `/home/user/dataset.bin`.

Your pipeline must be fully reproducible and executable by running `bash /home/user/run_pipeline.sh`. The final artifact `/home/user/dataset.bin` must be a sequence of 2-byte little-endian tokens.