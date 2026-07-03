You are acting as a data analyst and C++ developer for a network infrastructure team. We are mapping out a legacy network's topology to find the shortest latency paths between nodes.

We have partial data in a CSV file located at `/app/data/known_edges.csv`. 
Additionally, we recently recovered a field technician's voice memo, located at `/app/audio/network_intel.wav`. In this audio recording, the technician dictates several missing connections in the subnet that are not present in the CSV file. The format of the spoken data is typically "Node X connects to Node Y with a latency of Z". 

Your task involves the following pipeline:
1. **Audio Extraction:** Transcribe the audio file `/app/audio/network_intel.wav` to recover the missing edge connections. You may install and use transcription tools like Python's `openai-whisper` to accomplish this.
2. **Data Integration:** Analyze the schema of `/app/data/known_edges.csv`. Merge the edges extracted from the audio with the CSV data to project a complete, directed graph model. 
3. **C++ Query Engine:** Write a C++ program and compile it to exactly `/home/user/query_engine`. 
   - The program must load the materialized, unified graph data.
   - It must accept exactly two command-line arguments: `source_node` and `target_node` (both as integer IDs).
   - It must output a single integer to standard output: the shortest path latency between the source and target. If no path exists, it must output `-1`. 
   - Example invocation: `/home/user/query_engine 45 102`

You must ensure that your `query_engine` accurately traverses the directed graph using an algorithm like Dijkstra's. The resulting binary will be rigorously tested against thousands of random source and target pairs to ensure perfect equivalence with our reference implementation.