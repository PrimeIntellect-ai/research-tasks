You are a Database Reliability Engineer currently on call. We have a severe corruption in our production graph database, and our standard backup manifests have been destroyed. 

The previous on-call engineer left an automated voicemail detailing the specific entry point we need to recover, but they got cut off. 

You have the following resources:
1. `/app/voicemail.wav`: An audio recording from the previous engineer containing the target `node_id` that acts as the root for our critical missing data.
2. `/app/graph_backup.bin`: A raw, uncompressed binary dump of our graph database's adjacency list. 

Your objective is to extract the correct `node_id` from the audio and recover its outbound edges from the binary dump. 

**Data Model Constraints for `/app/graph_backup.bin`:**
The file is a packed binary file (Little Endian) consisting of contiguous records. Each record has the following structure:
- `node_id`: 32-bit unsigned integer (4 bytes)
- `edge_count`: 32-bit unsigned integer (4 bytes)
- `edges`: An array of `edge_count` 32-bit unsigned integers, representing the target node IDs this node connects to.

**Requirements:**
1. Determine the target `node_id` from the voicemail. You may use available tools (like Whisper, Python, or ffmpeg) to transcribe or listen to the audio.
2. Write a C program (e.g., `recover.c`) to parse the `graph_backup.bin` data model.
3. Your C program must locate the target `node_id` and iterate over its edges.
4. For each edge, generate a parameterized Cypher query string to reconstruct the relationship. 
5. Output these Cypher queries to exactly `/home/user/recovery.cypher`.

**Expected Output Format (`/home/user/recovery.cypher`):**
Each line should contain exactly one Cypher statement in the following format:
`CREATE (n:Node {id: <SOURCE_ID>})-[:CONNECTED_TO]->(m:Node {id: <TARGET_ID>});`

Replace `<SOURCE_ID>` with the node ID from the audio, and `<TARGET_ID>` with the extracted edge IDs.