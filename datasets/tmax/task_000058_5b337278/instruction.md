We are currently migrating our legacy data processing pipeline. The old system consists of a monolithic Python 2 script that parses structured timeseries data, calculates rolling averages, and sorts the output. We are modernizing this into a microservices architecture using a Python 3 API Gateway, a Go gRPC backend, and Nginx as a reverse proxy. 

Your task consists of two major parts: exact logic translation and service integration.

**Part 1: Core Logic Translation (Fuzz Equivalence)**
The legacy Python 2 script is located at `/app/legacy/process_v2.py`. It reads data from standard input and writes to standard output. 
The input format is a newline-separated list of records: `ID|Timestamp|val1,val2,val3,...`
The output format is `ID|Timestamp|AverageValue` (where AverageValue is mathematically rounded to exactly 3 decimal places). The output must be sorted chronologically by `Timestamp` (ascending), and then alphabetically by `ID` in case of a tie.

You must write a Go program that perfectly replicates this behavior. 
1. Create your Go code in `/home/user/migrated/`. 
2. Compile your standalone processing binary to `/home/user/migrated/processor`.
This binary will be rigorously tested against the legacy Python 2 script using thousands of randomly generated inputs to ensure bit-exact equivalence (the binary must read from stdin and write to stdout).

**Part 2: Multi-Service Composition**
Once the logic is ported, you must integrate it into our new architecture. We have provided a skeleton for the microservices in `/app/services/`:
- **Nginx**: Running on port `8080`.
- **Python 3 API Gateway**: A Flask app at `/app/services/gateway/app.py` running on port `5000`.
- **Go gRPC Backend**: You must implement the gRPC server in Go using the provided protocol buffer definition at `/app/services/proto/data.proto`. The gRPC server must listen on port `50051`.

You need to:
1. Implement the Go gRPC server (in `/home/user/migrated/server.go`) that imports your ported processing logic and serves the `ProcessData` RPC endpoint. 
2. Compile and run the gRPC server.
3. Fix the Python 3 Flask app (`/app/services/gateway/app.py`) so it properly calls your Go gRPC backend. You will need to compile the protobuf for Python 3 as well.
4. Configure Nginx (`/app/services/nginx/nginx.conf`) to route all HTTP POST requests sent to `http://localhost:8080/api/process` to the Python 3 Flask gateway. Start/reload Nginx.
5. Start the Python 3 Flask gateway.

When finished, an automated test will verify the fuzz-equivalence of your Go binary, and then send an end-to-end HTTP POST request containing raw data to `http://localhost:8080/api/process` to ensure the entire microservice chain (Nginx -> Flask -> Go gRPC) correctly processes the data and returns the expected structured response.