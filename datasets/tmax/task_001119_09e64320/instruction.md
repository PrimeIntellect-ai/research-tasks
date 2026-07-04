You are tasked with porting and fixing a legacy hybrid C/Go service so it can run in a minimal containerized environment. The project is located at `/home/user/project`. 

Currently, the build is completely broken due to three main issues:
1. **Broken C Library Makefile:** The C dependency located in `/home/user/project/clib` has a broken Makefile. It fails to compile the static library `libcore.a`. You must debug and repair the Makefile so it builds successfully.
2. **Circular Dependency:** The Go application has a circular import between the `server` package and the `config` package. You need to refactor the Go code to break this cycle without changing the overall functionality or exported API of the server.
3. **Conditional Build Issue:** The project contains a legacy telemetry module that fails to compile on minimal Linux environments. You must compile the Go application using the `minimal` build tag to exclude this module.

Additionally, the service requires an API Token and a specific port to bind to. These deployment parameters are not stored in the codebase; they are embedded as text inside an architecture diagram located at `/app/arch.png`. You must extract the API token and the port number from this image.

Your final objective is to:
1. Fix the Makefile and build `libcore.a`.
2. Resolve the circular import in the Go code.
3. Build the Go binary using `go build -tags minimal -o bin/server`. 
4. Run the compiled binary in the background. The binary takes two environment variables: `SERVER_PORT` (extracted from the image) and `API_TOKEN` (extracted from the image). 

Leave the server running in the background. It will serve an HTTP API, and we will automatically test its `/ping` endpoint to ensure it authorizes requests using the extracted token and returns the correct response.