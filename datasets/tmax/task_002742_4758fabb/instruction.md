You are a data engineer building an ETL and retrieval pipeline for video analytics. We need to extract features from a surveillance video, process them using a custom C program to ensure high performance, and serve them via a fast TCP socket server for downstream querying.

Here are the requirements:

**1. Data Extraction (Bash/FFmpeg)**
There is a video file located at `/app/surveillance.mp4`.
Extract the first 10 seconds of this video at exactly 1 frame per second (10 frames total). 
Resize the frames to exactly 320x240 pixels.
Save them as raw RGB24 video frames (no header, just interleaved R, G, B bytes) into `/home/user/frames/` with the naming convention `frame_01.raw` to `frame_10.raw`.

**2. Feature Engineering (C Program)**
Write a C program at `/home/user/etl/embed.c` that computes a 16-dimensional "embedding" for a given raw RGB frame.
The mathematical schema for the embedding is:
- Convert the RGB pixels to grayscale using the formula: `Gray = (0.299 * R) + (0.587 * G) + (0.114 * B)`. Store as a standard C `double`.
- Divide the 320x240 image into a 4x4 grid. Each grid cell will be 80x60 pixels.
- Cells are indexed 0 to 15, reading left-to-right, top-to-bottom.
- For each cell, compute the average Grayscale value of all pixels in that cell.
- The 16 average values form the 16-dimensional embedding of the frame.
Compile this program and use it to process all 10 frames, saving the results to a structured CSV at `/home/user/etl/embeddings.csv`. The CSV should have the format: `filename,v0,v1,...,v15` (values rounded to 2 decimal places).

**3. Retrieval Server (C Program)**
Write a C TCP server at `/home/user/etl/server.c` and run it in the background.
- It must listen on `127.0.0.1:9090`.
- It must load the data from `/home/user/etl/embeddings.csv`.
- When a client connects via TCP and sends a line ending in `\n` in the format:
  `SEARCH v0,v1,...,v15\n` (where v0..v15 are floating point numbers)
- The server must compute the squared Euclidean distance between the query vector and all 10 frame embeddings.
- It must reply with: `MATCH <filename>\n` corresponding to the frame with the smallest distance. 
- It must handle multiple sequential queries on the same connection, and close the connection if the client sends `QUIT\n`.

Ensure your server is running and bound to port 9090 before completing the task. We will test it by sending TCP requests.