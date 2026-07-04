You are a database administrator tasked with optimizing a slow graph traversal workflow. We have an SQLite database located at `/app/network.db` containing a large, unindexed collection of network edges in a messy format. 

Another team provided an architecture diagram at `/app/schema.png`. Use OCR tools (like `tesseract`, which is preinstalled) to read the text in this image. The image contains:
1. The target query requirements: "Find the shortest path sum from Node A to Node B" (the specific node IDs are written in the image).
2. The names of the source tables you must join and aggregate to form the actual graph.

Your task is to:
1. Parse the requirements from the image.
2. Create an optimized database at `/home/user/optimized.db`. You should project and materialize the messy network data into a clean, indexed graph representation (e.g., an `edges` table with `src`, `dst`, and `cost`).
3. Write a multi-language or shell-based script at `/home/user/compute_path.sh` that takes no arguments, connects to `/home/user/optimized.db`, computes the shortest path between the two nodes specified in the image, and outputs ONLY the total minimum cost (a single integer) to standard output. 

Your script must be highly optimized. Our automated test will run your `/home/user/compute_path.sh` script and compare its execution time against our unoptimized reference implementation. You must achieve a runtime speedup of at least 5.0x, and your output must exactly match the true shortest path cost.