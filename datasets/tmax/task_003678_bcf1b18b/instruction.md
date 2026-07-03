You are assisting a researcher in organizing a large dataset of animal foraging behavior videos and corresponding hierarchical taxonomy metadata. The data is currently messy, and the researcher needs to build a robust data pipeline, construct optimized queries, and filter out corrupted metadata.

Your tasks are:

1. **Video Frame Extraction**
A video file is located at `/app/foraging_behavior.mp4`. The researcher needs to index the keyframes. 
Use `ffprobe` to extract the presentation timestamps (in seconds) of all keyframes (I-frames) in the video. 
Save these timestamps to a CSV file at `/home/user/keyframes.csv`, with a single column `timestamp` sorted in ascending order.

2. **Adversarial Metadata Filtering**
The researcher has a directory of taxonomy metadata files in JSON format. Some files represent a valid taxonomy tree, while "corrupted" files contain cyclical references (where a node's parent chain loops back to itself).
- Clean corpus (valid trees): `/app/taxonomy_corpus/clean/`
- Evil corpus (contains cycles): `/app/taxonomy_corpus/evil/`
Each JSON file contains a list of dictionaries with keys `id` (integer) and `parent_id` (integer or null).
Write a script at `/home/user/cycle_detector.py` that takes a single file path as a command-line argument.
The script MUST:
- Exit with code `0` if the JSON file represents a valid tree/forest (no cycles).
- Exit with code `1` if the JSON file contains any cyclical references.

3. **Database Schema & Index Strategy**
Create a SQLite script at `/home/user/schema.sql` that sets up the database for this project. It must contain:
- A table `taxonomy` with `id` (INTEGER PRIMARY KEY), `parent_id` (INTEGER, foreign key to taxonomy.id), and `name` (TEXT).
- A table `keyframes` with `id` (INTEGER PRIMARY KEY), `video_name` (TEXT), and `timestamp` (REAL).
- An optimal index on `keyframes` to speed up range queries filtering by `video_name` and sorting/paginating by `timestamp`. Name this index `idx_keyframes_video_time`.

4. **Recursive Query Construction**
The researcher frequently needs to export the full path of each taxonomy node.
Create a SQL query file at `/home/user/recursive_export.sql`. This query must use a Recursive Common Table Expression (CTE) to output three columns:
- `id`: the id of the taxonomy node.
- `name`: the name of the taxonomy node.
- `path`: a string representing the full hierarchical path separated by ` > ` (e.g., "Animalia > Chordata > Mammalia").
Ensure the query fetches all nodes, even those at the root. Sort the final output by `id` ascending.