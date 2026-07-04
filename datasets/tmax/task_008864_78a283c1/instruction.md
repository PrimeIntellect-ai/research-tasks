You are an integration developer testing a mock internal microservices API. Your team relies on an API that provides service configuration data and dependency mappings to dynamically generate build system configurations.

First, start the mock API server that has been placed in your home directory by running:
`python3 /home/user/mock_api.py &`
This will start an HTTP server on `127.0.0.1:9090`.

Your task is to write a Python script that does the following:
1. Queries the endpoint at `http://127.0.0.1:9090/api/v1/dependencies` which returns a JSON array of services. Each service object contains `name`, `depends_on` (a list of service names it depends on), and `config_data` (a string).
2. Calculates the SHA-256 checksum for the `config_data` of each service. 
3. Resolves the dependency graph and determines a valid build order (topological sort, where dependencies are built before the services that depend on them). Write this ordered list of service names, comma-separated, to `/home/user/build_order.txt`. (If multiple valid topological sorts exist, any valid one is acceptable).
4. Generates a valid `Makefile` at `/home/user/Makefile` to automate the build process.
   - The first target in the Makefile must be `all: ` followed by all service names.
   - For each service, generate a target that lists its dependencies correctly.
   - The recipe for each service target must be exactly (note the tab indentation required by Make):
     `	echo "<sha256_checksum>" > <service_name>.build`

Verify your work by running `make -C /home/user` and ensuring the `.build` files are generated correctly with the right checksums.