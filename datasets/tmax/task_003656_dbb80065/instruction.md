We are in the process of porting a legacy Web Security API sequence validator to run in a minimal container. The validator checks if a sequence of API calls follows an allowed dependency graph. 

You need to complete the following steps:
1. We have an architecture diagram of the allowed API transitions in `/app/diagram.png`. Use `tesseract` to perform OCR on this image. It contains a list of allowed directed edges in the format `Source -> Destination` (one per line).
2. Go to the C++ project in `/app/validator/`. Modify the `initialize_graph()` function in `graph_config.cpp` to add the exact directed edges you extracted from the image. Use the existing `add_edge(src, dest)` API in the file.
3. The project has a `Makefile`, but running `make` currently fails due to a linking error related to threads and static libraries. Fix the `Makefile` so the project compiles successfully. 
4. The final executable must be built at `/app/validator/api_validator`.

When run, the executable takes a sequence of API endpoints as positional arguments (e.g., `/app/validator/api_validator login mfa session`). It will print `VALID` if every adjacent pair in the input sequence corresponds to a valid directed edge in the graph, and `INVALID` otherwise. Single-node inputs are always `VALID`. 

Do not print any additional debug information from the final executable.