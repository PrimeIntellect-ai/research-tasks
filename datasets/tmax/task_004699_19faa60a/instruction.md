You are tasked with setting up the build configuration for a polyglot data processing system. The system relies on gRPC for communication, but the schema definitions are updated frequently by different teams.

In the directory `/home/user/protos`, there are several protobuf files named following the pattern `service_<version>.proto`. The versions are standard Semantic Versions (e.g., `1.0.0`, `1.2.0-rc.1`).

Your objective is to:
1. Programmatically identify the `.proto` file with the highest semantic version.
2. Set up a new Go project in `/home/user/pipeline` with the module name `pipeline`.
3. Install the necessary Go protoc plugins (`protoc-gen-go` and `protoc-gen-go-grpc`).
4. Compile ONLY the protobuf file with the highest semantic version into Go code. The proto files specify `option go_package = "pipeline/api";`, so configure your `protoc` command to output the generated files correctly within your module.
5. Write a minimal Go program in `/home/user/pipeline/main.go`. This program must:
   - Import the generated `pipeline/api` package.
   - Define a struct that embeds `api.UnimplementedDataProcessorServer` (the service name in the proto is `DataProcessor`).
   - In its `main()` function, write the exact string `Successfully built service version <VERSION>` (replacing `<VERSION>` with the highest semantic version you identified, exactly as it appears in the filename) to the file `/home/user/pipeline/success.log`.
6. Run your Go program so that `/home/user/pipeline/success.log` is created.

Assume `protoc` and `go` are already installed on the system. Ensure your environment is configured so `protoc` can find the Go plugins (e.g., setting `PATH=$PATH:$(go env GOPATH)/bin`).