You are a QA engineer tasked with setting up automated test environments. To stand up a complex microservice architecture, the environment needs to start services in a specific dependency order. 

You have been provided a script located at `/home/user/service_resolver.py` that reads a dependency graph from `/home/user/dependencies.json` and performs a custom topological sort to determine the startup execution order. 

However, the script is currently failing. Due to the way the custom graph data structure and traversal are designed, it is consuming too much memory and crashing with a `MemoryError` before it can complete. The simulated test environment enforces a strict memory limit on this script.

Your task:
1. Debug and fix the memory leak/excessive memory usage in `/home/user/service_resolver.py` without removing the heavy state simulation (the `_mock_env_data` bytearray) in the `ServiceNode` instances. You must fix the traversal logic itself.
2. Ensure the script completes successfully and writes the correctly resolved execution order (comma-separated service names) to `/home/user/execution_order.txt`.
3. Do not change the traversal iteration order (it relies on `sorted(self.nodes.keys())`); only fix the memory footprint.

Run the script to verify it creates `/home/user/execution_order.txt` successfully.