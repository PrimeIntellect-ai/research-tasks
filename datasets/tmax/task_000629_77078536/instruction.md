You are a database researcher analyzing a visualization of concurrent transactions to identify deadlock states. 

A simulation tool has exported its transaction logs as a video file located at `/app/tx_visual.mp4`. In this video, each frame represents a discrete time step in the system. The simulation state is encoded purely in the uniform background color of the frames. 

To decode the events, you must read the color of the center pixel (x=width/2, y=height/2) for each frame in sequence. The RGB values (using an 8-bit per channel format) encode the following:
- **Red channel (R):** Transaction ID (1 to 255). If R=0, no event occurred in this frame.
- **Green channel (G):** Resource ID (1 to 255).
- **Blue channel (B):** Action type. 
  - `B=1`: The transaction *requests* the resource.
  - `B=2`: The transaction *acquires* the resource (meaning the lock is granted).
  - `B=3`: The transaction *releases* the resource.

Your task is to:
1. Parse the video to extract the chronological sequence of transaction events.
2. Reconstruct the state of the database locks at the end of the video. A resource can only be acquired by one transaction at a time. If a transaction requests a resource already acquired by another, it waits.
3. Build a Wait-For Graph (or equivalent representation) to model the dependencies between transactions and resources based on the final state.
4. Write a Python script at `/home/user/detect_deadlock.py` that takes a single integer command-line argument (a Transaction ID).
   - If the given transaction is involved in a deadlock cycle at the end of the video, your script must print exactly: `DEADLOCK: Tx<ID> -> Res<ID> -> Tx<ID> ...` representing the cycle of waits, starting and ending with the requested Transaction ID. (e.g., `DEADLOCK: Tx1 -> Res2 -> Tx2 -> Res1 -> Tx1`). Always output the cycle following the direction of requests.
   - If the transaction is not part of a deadlock cycle, print exactly: `NO DEADLOCK`.

You must correctly implement the graph traversal / complex recursive CTE logic to detect the cycles. The output of your script must be deterministic. If there are multiple branches in a cycle, assume standard lock acquisition ordering (FIFO for requests).