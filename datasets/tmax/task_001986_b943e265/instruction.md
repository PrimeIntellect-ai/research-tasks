You are an AI assistant helping a data researcher organize and process a temporal dataset from a recent experiment. 

We have a video recording of the experiment located at `/app/experiment_run.mp4`. The video contains a sequence of flashing barcodes (Code 128) on a screen, which encode edges in a knowledge graph representing protein interactions. Each barcode contains a string in the format `SourceNode-TargetNode-InteractionStrength` (e.g., `ProtA-ProtB-85`). Every edge appears exactly once in the video, with one edge shown per second (exactly on the second mark: 00:00:01, 00:00:02, etc.).

Your task is to:
1. Extract the frames exactly at every second mark using `ffmpeg` or Python (OpenCV/pyzbar).
2. Decode the barcodes to build a dataset of temporal protein interactions.
3. Load this data into an in-memory SQLite database (or persistent at `/home/user/graph.db`).
4. Bring up an HTTP REST API server using Python (Flask or FastAPI) listening exactly on `127.0.0.1:8555`.

The API must expose a single POST endpoint `/analyze` that accepts a JSON payload: `{"node": "ProteinName"}`.
When requested, the endpoint must execute a complex query combining window functions and recursive joins (knowledge graph traversal) to return the following JSON structure:
```json
{
  "direct_interactions": [
     {"target": "...", "strength": ...},
     ...
  ],
  "strongest_path_to_hub": "ProtA -> ProtB -> ProtHub",
  "rolling_avg_strength": 75.5
}
```
Where:
- `direct_interactions` lists all nodes the requested node interacts with as a source, ordered by descending strength.
- `strongest_path_to_hub` is the shortest path (by number of hops) to the node "ProtHub" in the graph. If there are ties, pick the path with the highest sum of interaction strengths.
- `rolling_avg_strength` is the average interaction strength of all edges involving the requested node (either as source or target), computed over the chronological sequence in which they appeared in the video.

Write a script `/home/user/serve_api.py` that accomplishes this and leave it running in the background. Do not exit until the server is successfully handling requests.