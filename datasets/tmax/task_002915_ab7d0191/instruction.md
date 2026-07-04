You are a data scientist working on fitting network models to molecular interaction graphs. You need to build a robust filtering tool to sanitize datasets of molecular graphs, distinguishing between valid network models and anomalous ("evil") ones.

First, there is an image located at `/app/model_spec.png`. This image contains printed text specifying the analytical parameters for our expected valid networks, specifically a target mean degree and a maximum distance metric threshold. You will need to extract this text (e.g., using `tesseract`).

Second, you have been provided with two directories containing training data:
- `/app/corpora/clean/`: Contains text files of valid graph edge lists.
- `/app/corpora/evil/`: Contains text files of invalid graph edge lists.
Each file contains one edge per line (two space-separated integers representing connected node IDs). The nodes are zero-indexed, and the networks are undirected. Assume N=100 nodes for all graphs.

Your objective is to create a Rust-based command-line tool that acts as a classifier/sanitizer.
1. Initialize a Rust project at `/home/user/graph_filter`.
2. The tool must take a single command-line argument: a path to a directory containing `.txt` graph files.
3. For each file, the tool must compute the empirical degree distribution of the graph.
4. Compare this empirical distribution against a theoretical Poisson distribution with the mean parameter extracted from the image.
5. Calculate the Kolmogorov-Smirnov (KS) statistic (the maximum absolute difference between the empirical CDF and theoretical CDF).
6. If the KS statistic is less than or equal to the threshold extracted from the image, the graph is considered valid.
7. The program must output to `stdout` exactly one line per file in the format: `ACCEPT filename.txt` or `REJECT filename.txt`.

You must ensure that your Rust tool successfully accepts 100% of the clean corpus and rejects 100% of the evil corpus. 

You can test your implementation using the provided corpora. The automated grading system will run your tool against these same corpora (and potentially hidden ones drawn from the exact same distributions).