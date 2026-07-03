You are tasked with building a C++ data comprehension tool to analyze transaction logs and detect potential deadlocks. 

A startup script `/app/start_services.sh` brings up a multi-service architecture comprising:
1. A transaction router (Flask, port 8000)
2. A simulated lock manager (Redis, port 8001)

Your goal is twofold:
1. **Configure the Services**: Edit `/home/user/app_config.yaml` so the transaction router connects to the lock manager at `127.0.0.1:8001` and uses your validator binary. The YAML should look like:
   ```yaml
   lock_manager_host: "127.0.0.1"
   lock_manager_port: 8001
   validator_binary: "/home/user/validate_queries"
   ```
2. **Implement the C++ Validator**: Write a C++ program at `/home/user/validator.cpp` and compile it to `/home/user/validate_queries`. 
   The program must accept a single command-line argument: the path to a CSV file.
   The CSV contains transaction logs with columns: `tx_id,resource_id,action` (with a header row).
   `action` is either `ACQUIRE` or `RELEASE`.
   
   Your C++ program must simulate the lock acquisitions in the exact order they appear in the CSV to detect deadlocks using a Wait-For Graph.
   - If a resource is free, `ACQUIRE` grants it to the `tx_id`.
   - If it is already held by another transaction, `tx_id` must wait (creating a directed edge `tx_id -> owner_tx_id`).
   - `RELEASE` frees the resource. If transactions are waiting for it, the one that requested it first gets it.
   - If at any point a cycle is formed in the Wait-For Graph, the program must immediately print `REJECT` to standard output and exit with code 1.
   - If the entire file is processed without cycles, print `ACCEPT` and exit with code 0.

Ensure your C++ program is compiled with `-std=c++17` or later.
Do not use any external libraries other than the C++ Standard Library.