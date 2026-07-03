You have just inherited an unfamiliar, legacy codebase located at `/home/user/legacy_sim`. This project is a Python-based scientific dependency simulator, but it is currently broken. Your goal is to debug the system, fix the code, recover a lost secret, and generate a final verified report.

Here is the context on the system's current state and your objectives:

1. **Test Failures due to Precision Loss**:
   The module `calculator.py` contains a function `compute_precise_sum(n)` that is supposed to add `0.1` together `n` times. However, because it uses standard floating-point arithmetic, the tests are failing due to precision loss. You must modify `compute_precise_sum` to use Python's built-in `decimal.Decimal` module so that the exact mathematical value is preserved and returned as a `Decimal` object.

2. **Recursion Limit Exceeded**:
   The module `tree_resolver.py` contains a function `count_nodes(start_node_id, graph_data)` that calculates the size of a dependency subgraph. The input graph `data/graph.json` contains cyclic dependencies. The current implementation does not track visited nodes, resulting in an infinite recursion / `RecursionError`. You must fix `count_nodes` to track visited nodes and return the correct count of unique nodes in the connected component.

3. **Git History Forensics**:
   To generate the final report, the script `generate_report.py` requires a secret decryption key. The original developer accidentally committed this secret key in `config.py` in an early Git commit, but later removed it in a subsequent commit to "hide" it. You must search the git history of the repository to recover this secret key.

**Instructions:**
1. Fix `calculator.py` to use `decimal.Decimal` so precision is perfectly maintained.
2. Fix `tree_resolver.py` to handle cyclic dependencies by implementing a `visited` set mechanism.
3. Recover the secret key from the Git repository's history.
4. Once the code is fixed and you have the key, run the report generator:
   `python generate_report.py <SECRET_KEY>`
5. The script will validate your fixes and output a final string. Write this exact output string to `/home/user/final_report.txt`.

Ensure `/home/user/final_report.txt` contains *only* the final success string. You may run `pytest` (if installed) or manually test the files as you work to verify your fixes.