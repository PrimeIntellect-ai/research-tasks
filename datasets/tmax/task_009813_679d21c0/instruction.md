I am setting up a polyglot build system from scratch for a new microservices architecture. Our system uses Go for high-concurrency data ingestion and Python for data science, communicating via gRPC. 

We have a protobuf schema located at `/home/user/project/schema/sensor.proto`. I need you to complete the build setup and create a Python test fixture to verify the generated code.

Please do the following:

1. Create a shell script at `/home/user/project/build.sh` that compiles the `sensor.proto` file for both Go and Python.
   - The Go generated files must be output to `/home/user/project/gen/go`. (Assume the `go_opt=paths=source_relative` option is used so it outputs cleanly).
   - The Python generated files must be output to `/home/user/project/gen/python`.
   - Your script must create these output directories if they do not exist.
   - Use `python3 -m grpc_tools.protoc` for Python generation and standard `protoc` for Go.

2. Create a Python test script at `/home/user/project/test_sensor.py` that verifies the Python build works and sets up a mock test fixture.
   - The script must import the generated `sensor_pb2` and `sensor_pb2_grpc` modules (you will need to ensure the import path allows this, e.g., by modifying `sys.path`).
   - Define a mock class `MockSensorService` that inherits from `sensor_pb2_grpc.SensorStreamerServicer`.
   - Implement the `FetchData` RPC method in your mock class. It should take `request` and `context` arguments and return an iterator (or yield) exactly 3 `sensor_pb2.SensorResponse` objects. Set the `value` field of these responses to `1.1`, `2.2`, and `3.3` respectively.
   - Instantiate your mock class, call `FetchData(sensor_pb2.SensorRequest(client_id="test"), None)`, and collect the responses.
   - If the mock successfully yields the 3 expected values, append the exact string `BUILD_AND_TEST_SUCCESS` to a log file at `/home/user/project/build.log`.

Make sure your `build.sh` is executable. You do not need to run the scripts, just create them perfectly. Our automated CI will run `./build.sh` followed by `python3 test_sensor.py` to verify your work.