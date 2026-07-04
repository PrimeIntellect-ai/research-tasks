You are a security data analyst responding to a simulated cyber threat. We have intercepted a video feed from a threat actor's monitoring system and extracted a large corpus of network traffic logs in CSV format. 

Your task consists of two parts: Signal Extraction and Graph Analysis.

**Part 1: Signal Extraction**
We recovered a video file at `/app/network_capture.mp4`. The threat actors encoded a critical threshold value into this video.
1. Use `ffmpeg` to extract the frames of this video.
2. Analyze the extracted frames. The threat actors used a basic visual sync signal: in certain frames, the top-left pixel (x=0, y=0) is pure red (RGB: 255, 0, 0). 
3. Count the exact number of frames where this pure red pixel appears at (0,0). This integer count is your target threshold, which we will call `MIN_BOTS`.
4. Write this integer alone to `/home/user/threshold.txt`.

**Part 2: Graph Analysis**
You must write a Python detection script at `/home/user/detect.py` that acts as a classifier for network traffic.
The script must take a single command-line argument: the path to a CSV file.
Each CSV file contains network edges with three columns: `source`, `target`, and `relation`. The `relation` is always either `COMMAND` or `ATTACK`.

Your script must:
1. Use an embedded Python graph database that supports the Cypher query language (we recommend installing `kuzu`).
2. Programmatically map the flat relational CSV representation into a property graph schema (e.g., create a Node table for IPs, and Edge tables for the relations).
3. Load the input CSV into this graph.
4. Construct and execute a parameterized Cypher query to detect a specific botnet topology:
   - A single root node (`master`) sends a `COMMAND` relation to *at least* `MIN_BOTS` distinct intermediate nodes (`bot`).
   - Every one of those specific `bot` nodes sends an `ATTACK` relation to the *exact same* destination node (`target`).
5. If the CSV graph contains one or more instances of this topology, print exactly `EVIL` to standard output.
6. If the topology is absent, print exactly `CLEAN` to standard output.
7. Your script must be efficient and able to process large graphs quickly using appropriate graph queries.

To complete the task, ensure your script is perfectly accurate. A hidden automated test suite will run your `/home/user/detect.py` against a large corpus of unseen CSV files to verify its accuracy and performance.