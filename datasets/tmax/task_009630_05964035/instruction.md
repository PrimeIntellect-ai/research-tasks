You are an integration developer responsible for testing a new microservice API architecture. The system requires generating a highly specific API token by resolving the service execution order and extracting state from memory dumps using a custom emulator protocol.

Your objective is to generate the final API token and save it to `/home/user/api_token.log`.

Here are the details of the environment:
1. **Dependency Graph (`/home/user/api_deps.txt`)**: 
   Contains pairs of services indicating dependencies. The first column is the dependency, and the second column is the dependent service. You must resolve the correct execution order (topological sort) starting from the service that has no dependencies.

2. **Simulated Memory Dumps (`/home/user/mem/*.dump`)**:
   Each service has a memory dump file (e.g., `/home/user/mem/auth_gateway.dump`). These files contain hex memory addresses and their corresponding stored values, representing the memory profile of the service at execution time. Format: `<ADDRESS> <VALUE>` (e.g., `0x0010 4A`).

3. **Emulator Scripts (`/home/user/scripts/*.emu`)**:
   Each service has a mini-emulator script (e.g., `/home/user/scripts/auth_gateway.emu`). These scripts contain proprietary instructions. Currently, the only instruction you need to interpret is `READ <ADDRESS>`. 

**Task:**
Write and execute a Bash-only script or command chain that:
1. Performs a graph traversal to determine the exact execution order of the services defined in `api_deps.txt`.
2. Following this execution order, reads the `.emu` script for each service.
3. Interprets the `READ <ADDRESS>` instructions by looking up the corresponding memory address in that service's `.dump` file.
4. Extracts the values for each read operation and concatenates them together into a single, continuous string (no spaces or newlines).
5. Writes the final concatenated string to `/home/user/api_token.log`.

Only use standard Bash built-ins, coreutils, and standard Linux CLI tools. Do not use external programming languages like Python.