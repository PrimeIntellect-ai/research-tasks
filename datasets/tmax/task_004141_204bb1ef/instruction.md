You are a database administrator and data engineer for a smart city traffic monitoring project. We have a data pipeline that processes vehicle tracking events, but it is currently running much too slowly. 

Your task consists of three parts:

1. **Video Processing**: We have a sample traffic video at `/app/traffic_video.mp4`. Use Python and `ffmpeg` (or `cv2`) to extract motion events. For every 30-frame segment of the video, compute the average pixel difference between consecutive frames. If the average difference exceeds 5.0, consider it a "high_traffic" event. Output these events as JSON objects to `/home/user/video_events.jsonl` with the schema: `{"segment_index": int, "status": "high_traffic"}`.

2. **Data Querying & Graph Analytics Integration**: I have provided a slow script at `/home/user/query_pipeline.py`. This script reads a large, provided file of JSON vehicle trajectories (`/app/trajectories.jsonl`), filters them based on complex NoSQL-like criteria, builds a routing graph using `networkx`, and computes the betweenness centrality of all traffic nodes to find the most critical intersections. 
The script is extremely inefficient. It loads all data into memory, uses nested loops for filtering, and rebuilds the graph multiple times.

3. **Optimization**: Optimize `/home/user/query_pipeline.py`. You may rewrite the querying logic, use proper index strategies (if you choose to load the data into an in-memory SQLite database instead of pure Python lists), and optimize the graph analytics. The output format (a printed JSON dictionary of node centralities) must remain exactly the same. 

Your optimized script must run significantly faster than the original. We will evaluate your success based on the execution speedup compared to the original unoptimized script. Write your optimized script to `/home/user/query_pipeline_optimized.py`.

Ensure your code is reproducible, correctly handles parameterized queries or filters, and properly sorts and paginates the internal results before building the graph, exactly as the original script intends.