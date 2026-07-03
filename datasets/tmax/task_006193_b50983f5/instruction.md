As a release manager, I am preparing our deployment pipelines for a massive migration. Our deployment target resolution is currently handled by a legacy Python script that parses a state machine defined in a text file to determine which deployment tier a specific rollout sequence should target.

We are migrating our deployment orchestrator to Go, and we need to wrap this logic in a gRPC service. 

I have created a workspace for you at `/home/user/deploy-manager`.
In this directory, you will find:
1. `legacy_parser.py`: The original Python implementation of the state machine parser.
2. `rules.txt`: The transition rules for the state machine.
3. `pb/rollout.proto`: The protocol buffer definition for the new service.
4. `server_test.go`: A comprehensive Go test suite that tests the gRPC server.

Your task is to:
1. Initialize a Go module in `/home/user/deploy-manager` named `deploy-manager`.
2. Generate the Go gRPC code from `pb/rollout.proto`.
3. Create `server.go` in `/home/user/deploy-manager` and translate the state machine logic from `legacy_parser.py` into Go.
4. Implement the `RolloutServiceServer` interface defined in the generated gRPC code within `server.go`. The server should read `rules.txt` upon initialization and use the translated logic to evaluate requests.
5. The gRPC server should listen on port `50051`.
6. Make sure your implementation passes the tests in `server_test.go`.
7. Once your server passes the tests, run the test suite and save the verbose output to a file exactly at `/home/user/deploy-manager/test_results.log`.

Requirements:
- Do not modify `server_test.go`, `rules.txt`, or `pb/rollout.proto`.
- Your Go server must faithfully replicate the state machine logic (including returning "REJECTED" for invalid transitions).
- Save the final test output using: `go test -v ./... > /home/user/deploy-manager/test_results.log`.