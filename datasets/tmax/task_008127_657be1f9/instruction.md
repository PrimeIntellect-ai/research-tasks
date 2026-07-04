You are a script developer working on integration testing utilities. Your team recently performed a schema migration on the backend gRPC service, which is currently running locally on `localhost:50051`. 

Your local documentation and prototype files are out of date. Specifically, the `CreateTask` RPC on the `task.TaskService` service now requires new fields that are not documented in your old `.proto` files. 

Your task:
1. The gRPC server running on `localhost:50051` has server reflection enabled. Use a tool like `grpcurl` to inspect the live service and discover the updated schema for the `CreateTaskRequest` message.
2. Based on the new schema, construct a valid JSON payload for the `CreateTask` endpoint. The payload must create a task with the following logical properties:
   - title: "Agent Test"
   - A priority level equivalent to the highest possible priority defined in the new schema's Enum.
   - At least one tag with the value "automation".
3. Write a bash script at `/home/user/run_test.sh` that uses `grpcurl` (or any other CLI tool of your choice) to send this request to `localhost:50051`. 
4. The script must output the server's JSON response and redirect it into a file named `/home/user/success.json`.
5. Ensure your script is executable. Run your script to generate `/home/user/success.json`.

The server enforces strict validation on the new fields. If your request does not match the migrated schema requirements, it will return an error. You have completed the task successfully when `/home/user/success.json` contains the successful `TaskResponse` from the server.