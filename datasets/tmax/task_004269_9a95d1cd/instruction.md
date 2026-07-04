You are a data engineer debugging a complex ETL pipeline backed by a graph database. Recently, concurrent transactions have been deadlocking, causing pipeline failures. 

You have been given two related tasks to resolve this issue:

**Part 1: Video Forensic Analysis**
We captured a screen recording of the pipeline monitoring dashboard during a deadlock event, located at `/app/pipeline_monitor.mp4`. The video flashes a sequence of transaction log entries on screen (one entry per frame, plain black text on white background). 
1. Extract the frames using `ffmpeg`.
2. Use OCR (e.g., `tesseract`) to read the log entries.
3. Parse the logs to reconstruct the final Wait-For Graph (WFG) representing which transactions hold which resources, and which transactions are waiting for which resources.
4. Export the resulting graph as a JSON file to `/home/user/video_graph.json` in the following format:
```json
{
  "edges": [
    {"from": "T1", "to": "R1", "type": "HOLDS"},
    {"from": "T2", "to": "R1", "type": "WAITS_FOR"}
  ]
}
```

**Part 2: Deadlock Detector (Adversarial Filter)**
To prevent future pipeline stalls, you must write a sanitization script that can pre-flight check a batch of transactions represented as a Knowledge Graph.
1. Create a script at `/home/user/detect_deadlocks.py` (or `.sh`, depending on your language choice).
2. The script must accept a single argument: the path to a JSON file formatted exactly like your `video_graph.json`.
3. The script must analyze the graph to detect resource deadlocks (i.e., cycles in the transaction Wait-For dependencies).
4. If the graph contains a deadlock, the script MUST output exactly `DEADLOCK` to standard output. If the graph is entirely free of deadlocks, it MUST output exactly `SAFE`.

Your script will be tested against a hidden suite of "clean" (safe) and "evil" (deadlocking) graph transaction schedules to ensure it flawlessly distinguishes between them.