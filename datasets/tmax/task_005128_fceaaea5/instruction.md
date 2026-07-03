I am working on migrating our data processing pipeline from Python 2 to Python 3. We have an old Python 2 script that takes a web access dependency graph, parses the URLs, and calculates a caching priority score for our assets. Because this pipeline processes millions of logs in production, porting it to Python 3 (which uses more memory for this specific task) is undesirable. Instead, I want you to rewrite this specific hot-path module in C.

Here are the requirements:

1. **Input Data**: A text file will be located at `/home/user/pipeline/access_graph.txt`. 
   Each line represents a dependency edge where an asset requests another asset, formatted as:
   `<Requesting_URL> <Target_URL> <Transition_Weight>`
   Example:
   `/api/v1/resource?asset=main_js&v=1.2 /api/v1/resource?asset=utils_js&v=1.0 0.75`

2. **URL Parsing**: For both the Requesting URL and the Target URL, you need to extract the value of the `asset` parameter. The URL format is standard, but the `asset` parameter could be anywhere in the query string. In the example above, the requesting asset is `main_js` and the target asset is `utils_js`.

3. **Graph Dependency & Numerical Scoring**:
   You need to calculate a simplified caching priority score for each unique asset found in the file (either as a requester or a target).
   - An edge `A B W` means asset `A` requests asset `B` with weight `W`. This represents a directed edge from `A` to `B`.
   - The caching score for any asset `N` is calculated as: 
     `Score(N) = 0.15 + 0.85 * (Sum of weights of all incoming edges TO N)`
   - If an asset has no incoming edges, its score is simply `0.15`.

4. **Implementation & Output**:
   - Write your C code in `/home/user/pipeline/scorer.c`.
   - Compile it to an executable named `/home/user/pipeline/scorer` using `gcc`.
   - When run (without arguments), the executable must read `/home/user/pipeline/access_graph.txt` and generate an output file at `/home/user/pipeline/scores.csv`.
   - The output file `scores.csv` must contain the calculated scores formatted as `asset_name,score`.
   - The score must be formatted to exactly 4 decimal places (e.g., `1.0000`).
   - The output file must be sorted alphabetically by the `asset_name` in ascending order.

Please write the C program, compile it, and run it to produce the `scores.csv` file. 

Note: You may use standard C library functions. Assume asset names are alphanumeric strings up to 64 characters long, and there are at most 1000 unique assets in the graph.