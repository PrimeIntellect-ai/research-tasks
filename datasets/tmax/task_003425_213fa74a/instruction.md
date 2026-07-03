You are tasked with analyzing a video capturing a simulated network traffic visualization and producing a specific time-series aggregation of the data using graph relationships.

We have a video file located at `/app/network_traffic.mp4`. This video is 100 frames long. In each frame, there is a QR code that encodes a single network transmission event in the format: `SourceNode,DestNode,Bytes` (e.g., `A,B,150`). The frame index (0-based) represents the time of the event.

Your objective is to:
1. Extract the transmission events from the video frames using Python (e.g., using `OpenCV` and `pyzbar`).
2. Map this data into a structured CSV file named `/home/user/traffic.csv` with the schema: `frame_id, source, destination, bytes`.
3. Use Python to perform an analytical aggregation: For each `destination` node, calculate the rolling sum of `bytes` received over a moving window of the last 3 frames (the current frame and the 2 preceding frames). If no data was received in a frame for a node, the bytes for that frame is 0.
4. Output the aggregated results to `/home/user/results.csv` with the schema: `frame_id, destination, rolling_bytes`. Include rows only for frames where the destination node actually received a transmission (but the rolling sum must correctly account for the 0s in empty frames within the window).
5. Write an equivalent Cypher query to a text file `/home/user/rolling_query.cypher` that would perform this exact CSV import and analytical window aggregation if run on a Neo4j database (assume APOC is available if needed, though standard Cypher is preferred).

Ensure your Python script runs end-to-end to generate `/home/user/results.csv`. Your final accuracy will be evaluated by comparing your `results.csv` against the ground truth using a Mean Squared Error (MSE) metric on the `rolling_bytes` column.