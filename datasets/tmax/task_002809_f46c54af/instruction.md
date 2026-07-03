You are acting as an integration developer. We have a multi-file Go project located at `/home/user/aggregator` that aggregates real-time trade data. 

The application is supposed to:
1. Connect to a WebSocket server to receive a stream of trade events (JSON format).
2. Parse these structured JSON messages.
3. Expose a REST API endpoint (`GET /stats`) that returns the aggregated volume per trading symbol.

Currently, the project fails to pass its integration tests (`go test ./...`) due to two primary issues, reminiscent of structural compile/runtime issues:
1. **Concurrency deadlock/blocking**: The WebSocket client's message processing loop is blocking the main execution thread, preventing the REST API from starting correctly and causing timeouts.
2. **Data parsing failure**: The application panics or fails to unmarshal incoming WebSocket JSON payloads because of a type mismatch in the data model.

Your task is to:
1. Navigate to `/home/user/aggregator`.
2. Analyze the code in `ws/client.go` and `models/trade.go` to identify and fix the concurrency and parsing bugs.
3. Run the integration tests using `go test -v ./...`.
4. Save the standard output of the test run to `/home/user/test_results.log`.

The integration tests in `main_test.go` are completely correct and must not be modified. You may only modify `ws/client.go` and `models/trade.go`. 

A successful execution means the tests pass without timing out or panicking, and the `/home/user/test_results.log` file ends with a successful `PASS` status.