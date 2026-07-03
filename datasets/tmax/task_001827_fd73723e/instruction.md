You are a data analyst investigating a series of network traffic captures represented as graphs. 

First, we have a video artifact located at `/app/network_capture.mp4`. This video contains a sequence of frames showing an evolving network graph. You need to use `ffmpeg` to extract the frames from this video. A simple python script `/app/extract_edges.py` is provided; if you pass a frame image to it, it outputs a CSV list of edges (Source, Target) present in that frame. You must process all frames to determine the average degree centrality of the network across the video.

Second, based on your findings, you must implement a anomaly detector in C++. We have two directories containing CSV files of graph edges:
- `/app/corpora/clean/`: Contains normal network traffic graphs.
- `/app/corpora/evil/`: Contains anomalous network traffic graphs (e.g., botnet topologies with abnormally high centrality).

Write a C++ program at `/home/user/detector.cpp` and compile it to `/home/user/detector`. 
Your program must accept a single command-line argument (the path to a CSV file) and print exactly one line to standard output: either `CLEAN` or `EVIL`.
The detector should parse the CSV, map the relational edge data into a graph structure, compute the maximum degree centrality of any node, and classify the graph as `EVIL` if this maximum exceeds the average degree centrality you found from the video by more than 50% (multiplier of 1.5).

Ensure your compiled C++ program is executable and relies only on the standard library.