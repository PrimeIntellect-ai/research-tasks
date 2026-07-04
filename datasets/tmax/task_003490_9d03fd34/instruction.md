As a research assistant, I need you to help organize and query a dataset from our recent crystallization experiment. We have a video artifact of the experiment and need to store its frame-by-frame data in a NoSQL database, then build a fast, parameterized query tool in C.

Here is the multi-step workflow:

1. **Environment Setup**:
   - Start a local MongoDB instance (e.g., using Docker: `docker run -d -p 27017:27017 mongo`).
   - Install the MongoDB C driver (`libmongoc` and `libbson`).

2. **Video Processing & Data Ingestion**:
   - We have a video at `/app/experiment.mp4`.
   - Extract the frame-by-frame data. For each frame, count the number of "bright" pixels. A pixel is considered bright if its grayscale value is strictly greater than 200.
   - You can use this exact method to read the video frames reliably: `ffmpeg -i /app/experiment.mp4 -f image2pipe -pix_fmt gray -vcodec rawvideo -` (assuming 1 byte per pixel). The video is 320x240 at 30 fps.
   - Insert this data into the MongoDB database `research`, collection `frames`. Each document MUST have exactly this schema:
     `{ "frame": <integer_index_starting_at_0>, "bright_pixels": <integer_count> }`

3. **Query Construction (C Program)**:
   - Write a C program at `/home/user/query_frames.c` and compile it to `/home/user/query_frames`.
   - The program must take exactly three integer command-line arguments: `<min_frame> <max_frame> <min_bright_pixels>`.
   - It must connect to the local MongoDB instance (`mongodb://localhost:27017`).
   - It must construct a NoSQL aggregation pipeline using `libmongoc` and `libbson` to:
     a) `$match`: Filter documents where `frame` is between `<min_frame>` and `<max_frame>` (inclusive) AND `bright_pixels` >= `<min_bright_pixels>`.
     b) `$sort`: Order the results by `frame` ascending.
     c) `$project`: Exclude the `_id` field, include only `frame` and `bright_pixels`.
   - The program must execute the aggregation pipeline and print the resulting BSON documents to `stdout` as a JSON array. If no documents match, print `[]`. The JSON formatting should output exactly one document per line, or a compact JSON array, but it must be valid JSON representing the list of matched documents. (Standard `bson_as_canonical_extended_json` or `bson_as_relaxed_extended_json` output combined into an array format `[ {..}, {..} ]` is expected).
   - Ensure the program exits with code 0 on success.

Please complete the setup, data ingestion, and write the C program.