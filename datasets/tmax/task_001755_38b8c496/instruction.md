You are helping a data researcher organize a complex dataset. The researcher has recorded an audio memo detailing the dependencies between different data variables. 

There are two main objectives:

1. **Extract the Graph:** 
   You have been provided with an audio file at `/app/dataset_memo.wav`. This file contains spoken English describing the connections in the dataset (e.g., "Node A connects to Node B"). 
   You must transcribe this audio and create a directed edge list file at `/home/user/graph.txt`. Each line should represent a directed edge in the format `Source,Target` (e.g., `A,B`).

2. **Fix the Graph Query Engine:**
   The researcher wrote a Go program located at `/home/user/graph_tool.go` to materialize a graph projection from the edge list and serve query results. Specifically, it reads the edge list file, then enters a loop reading node names from standard input. For each node, it is supposed to output its 2-hop neighborhood (all nodes reachable in exactly 1 or 2 directed steps) as a comma-separated list, sorted alphabetically.
   
   However, the researcher's graph materialization logic contains a critical bug: it performs an implicit cross-join when trying to find paths, resulting in incorrect and massive result sets.
   
   Your task is to fix `/home/user/graph_tool.go` so that it correctly computes the 2-hop neighborhood. The program must take the edge list file path as its first command-line argument, read node queries from `stdin` (one per line), and print the sorted 2-hop neighborhood to `stdout` (one line per query).

Build your fixed program and save the executable to `/home/user/graph_query`.

Constraints & Requirements:
- Use Go for the graph query engine.
- You may use any available tools (e.g., `whisper.cpp`, `ffmpeg`, Python libraries) to transcribe the audio. 
- The format of `/home/user/graph.txt` must be strictly `Source,Target` per line.