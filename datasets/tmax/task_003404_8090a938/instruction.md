You are assisting a researcher who is organizing and analyzing a dataset of directed citation networks. 

The researcher has left a voice memo at `/app/lab_notes.wav` detailing some recent discoveries. Specifically, they identified exactly three "corrupted" nodes (representing plagiarized papers) that must be completely excluded from all future dataset analytics and shortest-path routing.

Your task is to implement a high-performance C++ query tool that calculates the shortest path between papers, strictly bypassing the corrupted nodes mentioned in the audio.

Requirements:
1. Listen to or transcribe `/app/lab_notes.wav` to identify the integer IDs of the three corrupted nodes. You may install any command-line tools or Python packages needed to transcribe the audio.
2. Read the directed graph dataset located at `/app/citations.txt`. The file contains space-separated integers on each line representing an edge: `source target weight`.
3. Write a C++ program that reads this graph and accepts routing queries via standard input (`stdin`). 
4. Each line of `stdin` will contain two space-separated integers: `start_node end_node`.
5. For each query, calculate the shortest path distance from `start_node` to `end_node` using Dijkstra's algorithm. You must NOT route any paths through the three corrupted nodes (they effectively do not exist).
6. Output the shortest distance as an integer on a new line to `stdout`. If the target is unreachable (or if the start/target is a corrupted node), output `-1`.
7. Your code must be written to `/home/user/pathfinder.cpp` and compiled to `/home/user/pathfinder`.

The tool will be tested extensively with automated queries to ensure it perfectly matches the expected behavior for thousands of random routing requests. Ensure your graph traversal is efficient and strictly adheres to the exclusion list.