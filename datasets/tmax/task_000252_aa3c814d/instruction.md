You are a cloud architect migrating an old, monolithic service to a modern microservices architecture. Part of the legacy infrastructure relies on a proprietary routing metric calculator that processes link-state data to determine the optimal deployment paths for new microservices. 

The legacy calculator is a compiled binary located at `/app/legacy_router`. It has become a severe bottleneck in our deployment pipeline. When provided with a network topology file, a start node, and an end node, it calculates the optimal path and its "total cost" based on some internal weighting of network metrics.

Your task is to reverse-engineer the logic of the legacy calculator and write a highly optimized C++ replacement. 

1. Analyze the behavior of `/app/legacy_router`. 
   Usage: `/app/legacy_router <topology_file> <start_node> <end_node>`
   The topology file contains lines formatted as: `<LinkID> <NodeA> <NodeB> <Latency_ms> <Jitter_ms> <DropRate_percent>`

2. Write a C++ replacement at `/home/user/fast_router.cpp` and compile it to `/home/user/fast_router`.
   - Your replacement must accept the exact same command-line arguments and produce the EXACT same standard output as the legacy binary for any valid input.
   - You must deduce the internal formula the legacy binary uses to calculate the "cost" of a link from the Latency, Jitter, and DropRate metrics. 
   - You must deduce the routing algorithm used (e.g., shortest path based on that cost).

3. Optimize your C++ implementation. The legacy binary is extremely slow (it was poorly written and scales terribly with the number of nodes/edges). Your C++ program must achieve a significant speedup. We will evaluate your program against a massive hold-out topology graph with 100,000 edges.

Create your C++ source file, compile it, and ensure the executable is placed at `/home/user/fast_router`. It must run standalone without invoking the legacy binary.