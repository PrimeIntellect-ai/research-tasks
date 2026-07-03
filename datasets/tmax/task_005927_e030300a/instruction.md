You are a capacity planner analyzing a recent network misconfiguration where new Docker Compose services failed to start due to IP address space exhaustion and routing conflicts. 

Your organization tracks all assigned container network subnets in a JSON file located at `/home/user/allocations.json`. You have just received a proposed `/home/user/docker-compose.yml` file from the development team.

Your task is to write a Python script at `/home/user/planner.py` that automates the detection of subnet routing conflicts. The script must:
1. Parse the existing subnet allocations from `/home/user/allocations.json`.
2. Parse the requested custom network subnet(s) from the `/home/user/docker-compose.yml` file.
3. Use Python's built-in `ipaddress` module to check if any requested subnet overlaps with an existing allocated subnet.
4. If an overlap is found, the script must write a single line to `/home/user/report.txt` in the exact following format:
   `Conflict: requested <requested_subnet> overlaps with <existing_network_name> (<existing_subnet>)`

If multiple conflicts exist, record only the first one encountered. If no conflicts exist, write `No conflicts found` to the file. 

Run your script to generate the `/home/user/report.txt` file so your results can be verified.