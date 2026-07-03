You are an AI assistant helping a network science researcher organize and validate temporal graph datasets. We have recorded a dynamic network experiment as a video, and we also have a large repository of synthetic temporal graphs. We need to extract the experimental graph, understand its data model, and write a filter to sanitize our repository.

**Step 1: Graph Projection from Video**
We have a video of a temporal network experiment located at `/app/experiment_001.mp4`. 
- The video is exactly 10x10 pixels and 50 frames long.
- It encodes an adjacency matrix evolving over time. Each pixel `(y, x)` represents a directed edge from node `y` to node `x` (0-indexed, y is the row, x is the column). 
- An edge exists in a given frame if the average RGB pixel value at that coordinate is strictly greater than 128. 
- Ignore self-loops (where y == x).
Extract the frames (e.g., using `ffmpeg`) and write a Python script to parse these pixels into a materialized edge list. Save it to `/home/user/video_graph.csv` with exactly the columns: `frame`, `source`, `target` (in that order, comma-separated, with a header).

**Step 2: Corpus Sanitization (Adversarial Filter)**
We have collected many other temporal graph CSV datasets, but our data generation pipeline was bugged. Some datasets violate the physical constraints of our experimental model.
You must write a Python filtering script at `/home/user/filter_datasets.py` with the following signature:
`python3 /home/user/filter_datasets.py <input_dir> <output_dir>`

This script must:
1. Iterate over all `.csv` files in `<input_dir>`.
2. Validate the schema (files must contain exactly `frame`, `source`, `target` columns).
3. Apply the following temporal constraint using window functions or rolling aggregations:
   - A dataset is **VALID** if no single node is involved in more than **7** edges (counting both outgoing and incoming edges for that node) across **any sliding window of 5 consecutive frames** (e.g., frames 0-4, 1-5, 2-6, etc.). 
   - Note: The `frame` column may have gaps or missing frames; the sliding window is based on the numeric value of the frame index (e.g., a window starting at frame 2 strictly covers frames 2, 3, 4, 5, and 6).
4. If a file is VALID, copy it exactly as-is into `<output_dir>`. If it is INVALID (violates the constraint or schema), do not copy it.

**Testing Your Filter**
To help you develop and verify your logic, there are two test corpora provided on the system:
- `/app/corpus/clean/`: Contains ONLY valid datasets.
- `/app/corpus/evil/`: Contains ONLY invalid/corrupted datasets.

Your script must perfectly separate them. Test your script by running it against both directories to ensure it accepts 100% of the clean files and rejects 100% of the evil files.