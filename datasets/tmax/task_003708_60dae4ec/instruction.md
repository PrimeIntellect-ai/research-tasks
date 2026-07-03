You are an advanced database administrator tasked with optimizing a custom graph query engine for video stream analysis. 

We have a video file located at `/app/video.mp4`. We need to analyze the decoding dependencies of its frames and serve this data via a fast C++ web service.

Video frames have different types (I, P, B) and decoding dependencies. You must extract the frame sequence and sizes, build a dependency graph, and write a C++ HTTP server that calculates the recursive size of all frames required to decode a given frame.

### Step 1: Data Extraction
Use `ffprobe` (or similar tools) to extract the sequence of video frames from `/app/video.mp4`. 
For each frame, you need its `coded_picture_number` (which acts as its 0-based integer ID), its `pict_type` (I, P, or B), and its `pkt_size` in bytes.

### Step 2: Graph Dependency Rules
Build a directed graph of frame dependencies based on the following synthetic rules (assuming frames are ordered by `coded_picture_number`):
- **I-frames** do not depend on any other frames.
- **P-frames** depend on the single most recent 'I' or 'P' frame that appears *before* it in `coded_picture_number` order.
- **B-frames** depend on the most recent 'I' or 'P' frame *before* it, AND the earliest 'I' or 'P' frame *after* it in `coded_picture_number` order.

### Step 3: Recursive Query Engine
Write a C++ HTTP server (you may use a header-only library like `cpp-httplib` or raw sockets, standard C++17 allowed) that loads this graph and listens on `127.0.0.1:8080`.
The server must implement a recursive graph query accessible via:
`GET /dependency_size?frame=<N>`

Where `<N>` is the `coded_picture_number`. 
The endpoint must return an HTTP 200 response with a plain text body containing a single integer: the **sum of the `pkt_size`** of frame `<N>` AND all the unique frames it recursively depends on. 
*(For example, if frame 2 depends on frame 1, and frame 1 depends on frame 0, the result for frame 2 is the sum of sizes of frames 0, 1, and 2).*

Your server must run continuously in the background so it can be queried by our automated verification suite.