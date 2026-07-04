You are an expert data analyst investigating a routing anomaly. 

We have a simulation video of a packet traversing our network located at `/app/routing_sim.mp4`. The video plays at 1 frame per second (1 fps) for 5 seconds. In each second, the video displays a large, black integer on a white background representing the active Node ID the packet is currently visiting.

You also have a SQLite database at `/home/user/network.db` containing two tables:
- `nodes` (id INTEGER, name TEXT)
- `links` (source_id INTEGER, target_id INTEGER, distance INTEGER)

A previous analyst attempted to dump the edge list using the SQL query in `/home/user/export_edges.sql`, but they made a mistake (an implicit cross join), resulting in bloated and incorrect data.

Your task:
1. Fix the SQL query to correctly extract the edges (source_id, target_id, distance).
2. Extract the sequence of Node IDs from `/app/routing_sim.mp4` (you may use `ffmpeg` and `tesseract` (OCR) or any other tool).
3. Compute the total distance of the exact path traversed by the packet in the video using the corrected edge distances.
4. Output the final computed total distance as a single numerical value in `/home/user/total_distance.txt`.

Ensure your pipeline is robust. You have full access to bash, sqlite3, ffmpeg, tesseract-ocr, and standard Linux utilities to chain this process together.