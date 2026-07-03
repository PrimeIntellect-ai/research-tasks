You are a data analyst working with a custom hierarchical data structure representing a network of microservices. You have been given two CSV files detailing the services and their dependencies. 

Your task is to write a Rust program that reads these CSV files, reconstructs the dependency graph, and calculates the "Cumulative Cost" of each service. 

**Definitions:**
- **Cumulative Cost**: The Cumulative Cost of a service is its own `base_cost` plus the sum of the Cumulative Costs of all services it directly depends on.
- The dependency graph is guaranteed to be a Directed Acyclic Graph (DAG). 

**Input Files:**
1. `/home/user/services.csv`
   - Format: `id,base_cost`
   - Example: `service_A,100`
2. `/home/user/dependencies.csv`
   - Format: `service_id,depends_on_id`
   - Example: `service_A,service_B` (meaning service_A depends on service_B)

**Requirements:**
1. Write a Rust program at `/home/user/calculate_costs.rs`. You may compile it using `rustc calculate_costs.rs` (assume no external crates like `csv` are strictly required if you parse the simple comma-separated lines manually, though you can initialize a cargo project if you prefer).
2. The program must read the two CSV files.
3. It must calculate the Cumulative Cost for every service.
4. It must identify the service with the highest Cumulative Cost.
5. The program must output the result to a file at `/home/user/highest_cost.txt` in the exact format: `[SERVICE_ID]:[CUMULATIVE_COST]` (e.g., `service_A:450`). If there is a tie, output any one of the tied services.

Please write the Rust code, compile it, run it, and ensure the output file is generated correctly.