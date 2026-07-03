You are a Mobile Build Engineer responsible for maintaining and upgrading our remote build execution pipeline. Our pipeline relies on a mix of legacy native C++ tools and modern microservices. You have a multi-phase task to complete.

**Phase 1: Fix Legacy Build Tool (C/C++ Memory Safety)**
We have a legacy C++ tool located at `/home/user/build_tools/manifest_parser.cpp` that parses dependency manifests. Currently, it fails with segmentation faults and memory leaks due to undefined behavior (out-of-bounds array access and un-freed memory). 
1. Fix the memory safety issues and undefined behavior in `/home/user/build_tools/manifest_parser.cpp`.
2. Compile it to `/home/user/build_tools/parser_bin` using `g++`.

**Phase 2: Design gRPC/Protobuf Service**
We are migrating our dependency resolution to a new gRPC microservice.
1. Create a protobuf file at `/home/user/pipeline/build_service.proto` with a service `DependencyResolver`.
2. Define an RPC method `ResolveBuild` that takes a `ResolveRequest` and returns a `ResolveResponse`.
3. `ResolveRequest` must contain a repeated string field `requested_modules`.
4. `ResolveResponse` must contain a map<string, int32> `resolved_versions` and a double `build_priority_score`.

**Phase 3: Implement the Service (Constraint Satisfaction & Numerical Algorithm)**
Write and run a gRPC server in any language of your choice that implements the `DependencyResolver` service, listening on `localhost:50051`.
The server must implement the following logic when `ResolveBuild` is called:

1. **Constraint Satisfaction:**
   Given a list of requested modules, resolve their versions (integers). We have 4 available modules in our mobile monorepo: `Core`, `UI`, `Network`, and `Database`. 
   The versions must satisfy these strict constraints:
   - `Core` versions available: 1, 2, 3
   - `UI` versions available: 1, 2
   - `Network` versions available: 2, 3
   - `Database` versions available: 1, 2, 3
   - If `UI` == 2, then `Core` must be >= 2.
   - `Network` and `Database` versions must strictly equal each other.
   - The sum of all resolved versions must exactly equal 9.
   - Find the single valid combination of versions that satisfies all these constraints for the requested modules. (Assume requests will always ask for all 4 modules).

2. **Numerical Algorithm (Build Priority Score):**
   Calculate the `build_priority_score` using this formula: 
   Score = (Core_version * 1.5) + (UI_version * 2.5) + (Network_version * 3.5) + (Database_version * 4.5)

**Phase 4: Execution & Verification**
Write a client script that calls your running gRPC server with a `ResolveRequest` containing `["Core", "UI", "Network", "Database"]`.
The client must write the exact JSON representation of the `ResolveResponse` map and score to `/home/user/pipeline/resolution.json` in this exact format:
```json
{
  "versions": {
    "Core": X,
    "UI": Y,
    "Network": Z,
    "Database": W
  },
  "score": S.S
}
```

Make sure all services are installed, your server is running, and the output file is generated correctly.