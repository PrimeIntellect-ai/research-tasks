You are tasked with fixing a buggy Python algorithmic module and writing an end-to-end test orchestrator to verify the fix.

In `/home/user/`, you will find two files:
1. `algo.py`: Contains a function `longest_path(graph, start_node)` that calculates the maximum weighted path length in a Directed Acyclic Graph (DAG) starting from `start_node`.
2. `tests.json`: Contains serialized test cases. Each test case is a dictionary with `id`, `graph`, `start`, and `expected` fields.

The `longest_path` function currently has a bug that causes it to fail on certain valid inputs. 

Your objectives:
1. Write a Python script at `/home/user/test_orchestrator.py` that:
   - Deserializes the test cases from `/home/user/tests.json`.
   - Iterates through the tests, executing `longest_path(graph, start)` for each.
   - Compares the returned result to the `expected` value.
   - Serializes the results to `/home/user/results.json`. The output format must be a single JSON object mapping the string representation of the test `id` to a boolean indicating if the test passed (e.g., `{"1": true, "2": true}`).
2. Run your orchestrator to discover the bug in `algo.py`.
3. Fix the bug in `/home/user/algo.py` so that all test cases pass without crashing.
4. Run `/home/user/test_orchestrator.py` one final time to generate the successful `/home/user/results.json`.