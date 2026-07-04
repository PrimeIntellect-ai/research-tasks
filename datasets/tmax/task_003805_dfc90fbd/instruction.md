You are a performance engineer tasked with profiling and hardening a new statistical simulation package for analyzing Markov Chain Monte Carlo (MCMC) graph properties.

Part 1: Fix the Vendored Package
We have vendored the source for `mcmc_graph_solver` (version 1.0) under `/app/mcmc_graph_solver`. You need to install it in editable mode.
During our regression testing, we noticed that `pytest /app/mcmc_graph_solver/tests/test_reproducibility.py` fails randomly. The simulation produces non-reproducible stationary distributions due to floating-point reduction order variations. 
Your investigation should focus on how `mcmc_graph_solver/core.py` extracts unique nodes from the input edge list to build the transition matrix. Apply the necessary code fix to ensure the state matrix is constructed deterministically every time, which will make the test pass reliably.

Part 2: Adversarial Corpus Filtering
The simulation solver frequently crashes in production or gets stuck in infinite MCMC sampling loops when fed non-ergodic graphs (graphs that are not strongly connected, meaning not every node can reach every other node, or containing absorbing states).
You must write a Python classifier script at `/home/user/graph_filter.py` that reads a graph JSON file and validates it.

The JSON format is a dictionary representing an adjacency list, e.g.:
`{"1": [2, 3], "2": [1], "3": [1]}`

Requirements for `/home/user/graph_filter.py`:
- It must take exactly one argument: the path to a JSON graph file.
- It must perform graph analysis to determine if the Markov chain is ergodic (strongly connected).
- It must exit with code `0` if the graph is valid (clean).
- It must exit with code `1` if the graph is invalid/non-ergodic (evil).

We have provided two test directories to validate your script:
- `/app/corpora/clean/` contains valid, perfectly ergodic graphs.
- `/app/corpora/evil/` contains graphs with absorbing states, disconnected components, or one-way traps.

Your script will be tested against these exact corpora by our automated verifier.