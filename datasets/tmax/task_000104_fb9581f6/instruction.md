You are an AI assistant helping a bioinformatics researcher organize a large collection of biological pathway datasets. 

We have a massive dataset of interaction graphs, but many of them are corrupted or represent invalid biological pathways. Your task is to write a C++ program that acts as a strict filter to distinguish between valid ("clean") and invalid ("evil") pathway graphs.

Here is what you need to do:
1. Parse the schema constraints from an image. I have left an image at `/app/pathway_schema.png` which contains a text description of the valid edge transitions in our knowledge graph and a maximum path length constraint. You will need to extract these rules.
2. Reverse engineer the data model of the graphs. The graphs are provided as space-separated text files where each line represents a directed edge: `<Source_NodeType> <Source_NodeID> <Target_NodeType> <Target_NodeID>`.
3. Write a C++ program at `/home/user/graph_filter.cpp` and compile it to `/home/user/graph_filter`. 
4. The program must take a single command-line argument (the path to a graph text file).
5. The program must print exactly `ACCEPT` (followed by a newline) and exit with code 0 if the graph is valid. It must print exactly `REJECT` (followed by a newline) and exit with code 1 if the graph is invalid.

A graph is considered VALID ("clean") if and only if BOTH of these conditions are met:
- All edges in the graph conform to the valid transitions extracted from the schema image. Any graph with an edge transition not explicitly allowed by the schema is invalid.
- There exists at least one valid shortest path from a node of type `GENE` to a node of type `PATHWAY` that does not exceed the maximum path length specified in the image.

Compile your program using `g++ -O3 -std=c++17 /home/user/graph_filter.cpp -o /home/user/graph_filter`. Ensure your code is robust against malformed lines or disconnected components.