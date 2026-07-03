You are tasked with building a video analysis and similarity retrieval pipeline in Rust. 

We have a video file located at `/app/video.mp4`. Your goal is to process this video, extract visual features, handle missing data through strict schema enforcement, reduce the dimensionality of the features, and perform a similarity search.

Here is the exact workflow you must implement:

1. **Frame Extraction**: Use `ffmpeg` to extract frames from `/app/video.mp4` at exactly 1 frame per second (1 fps). Save them as JPEGs in `/tmp/frames/` with the naming convention `frame_0001.jpg`, `frame_0002.jpg`, etc.

2. **Feature Extraction & Schema Enforcement (Rust)**:
   Write a Rust application (you can use `cargo init`) that reads these frames in order. For each frame, compute a 64-bin grayscale histogram (where each bin represents a range of 4 pixel values, e.g., 0-3, 4-7, ... 252-255). Normalize the histogram so it sums to 1.0. 
   *Data Corruption Simulation*: If a frame's average pixel intensity is less than 10.0, it is considered a "corrupted" frame. Instead of outputting the histogram, your pipeline must initially flag these as `NaN` values.
   *Schema Enforcement*: You must enforce a schema of `(frame_id: u32, bins: [f64; 64])`. For corrupted frames, implement an imputation strategy where the `NaN` bins are replaced by the exact average of the strictly previous and strictly next valid frames' histograms.

3. **Dimensionality Reduction (Rust)**:
   Using a Rust crate like `linfa` or standard matrix operations (`nalgebra`/`ndarray`), perform Principal Component Analysis (PCA) on the (imputed) 64-dimensional dataset to reduce it to exactly 4 dimensions. 

4. **Similarity Search (Rust)**:
   In this 4-dimensional space, calculate the Euclidean distance between frames. 
   For the following query frames: `10`, `20`, `30`, `40`, and `50`, find the top 5 most similar frames (i.e., the 5 frames with the smallest Euclidean distance to the query frame, EXCLUDING the query frame itself).

5. **Output**:
   Your Rust program must output a CSV file at `/home/user/similarities.csv` with exactly this header:
   `query_frame,sim_1,sim_2,sim_3,sim_4,sim_5`
   It should contain 5 rows (one for each query frame: 10, 20, 30, 40, 50). The similar frames should be represented by their integer `frame_id` (1-indexed, matching the `ffmpeg` extraction numbers), ordered from most similar to least similar.

Focus on creating a robust, compilable Rust project. You are free to use any open-source crates (e.g., `image`, `ndarray`, `linfa`, `csv`).