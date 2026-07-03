You are an environmental researcher organizing sensor datasets. You have received a corrupted data transmission encoded as a video file located at `/app/sensor_feed.mp4`. 

Your goal is to extract the data from the video, load it into a SQLite database, and write a Go program to perform complex hierarchical and windowed time-series analysis. 

### Part 1: Data Extraction
The video (`/app/sensor_feed.mp4`) contains a sequence of uniform-color frames. Each frame represents a single sensor reading at a specific `frame_idx` (starting at 0 for the first frame).
Extract the average Red (R), Green (G), and Blue (B) color channel values for each frame (rounded to the nearest integer 0-255).
- **R channel**: Represents the `node_id`. (If `node_id` is 0, ignore the frame completely).
- **G channel**: Represents the `parent_id` of the node in the sensor hierarchy. (`parent_id` = 0 means it is a root node). The hierarchy is static, but transmitted redundantly.
- **B channel**: Represents the sensor `value` for that frame.

Load this data into a SQLite database located at `/home/user/sensor_data.db` with a table `readings(frame_idx INT, node_id INT, parent_id INT, value INT)`.

### Part 2: Hierarchical & Windowed Analysis (Go & SQL)
Previously, your team tried to calculate the "ancestral average" using a SQL query with an implicit cross join (`FROM readings r1, readings r2...`), which produced massively inflated incorrect results and ran exceptionally slowly.

Write a new Go program at `/home/user/analyze.go` that queries the SQLite database using modern SQL features (Recursive CTEs and Window Functions) to calculate the following for every valid frame reading:

1. **Path-Smoothed Value**: For a given reading at `frame_idx`, use a Recursive CTE to find the node and all of its ancestors (up to the root) based on the `parent_id` relationships. Calculate the average of the sensor `value`s of the node and its ancestors *for that specific reading event*. (Assume the ancestors' values are just their historical IDs if they don't have a reading in this exact frame; actually, to simplify: just average the `value`s of the node itself and the `value`s of its ancestors recorded at *any* prior `frame_idx` closest to this one. Wait, to make it perfectly deterministic: The `parent_id` merely defines the tree structure. The "Path-Smoothed Value" is defined as: the average of the `node_id`s of the node and all its ancestors. PLUS the `value` of the current reading). Let's use a simpler, strict definition:
   *Path-Smoothed Value* = The current reading's `value` + the count of its ancestors (i.e., its depth in the tree, where root has depth 0).
2. **Moving Average**: Using a Window Function, calculate the 3-frame rolling average of the *Path-Smoothed Value* for each `node_id`, ordered by `frame_idx` (the current frame and the 2 preceding frames for that specific `node_id`).

Your Go program must output the final results to `/home/user/results.csv` with the headers: `frame_idx, node_id, rolling_avg`. The `rolling_avg` should be formatted to 2 decimal places.

Ensure your Go program compiles and runs successfully, outputting the CSV.