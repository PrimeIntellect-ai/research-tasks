I have a messy project folder with several gRPC Protocol Buffer (`.proto`) files in `/home/user/protos`. I need you to help me organize and test them.

Here is what you need to do:

1. **Dependency Analysis (Graph Traversal):**
   Analyze the `.proto` files in `/home/user/protos`. Write a script to parse the `import "..."` statements and generate a JSON file at `/home/user/proto_graph.json`. The JSON should be a dictionary mapping each `.proto` file name (e.g., `"user.proto"`) to a list of the filenames of its direct imports (e.g., `["base.proto"]`). If a file has no imports, map it to an empty list `[]`.

2. **Build and Link:**
   Create a directory at `/home/user/generated`. Use `grpcio-tools` to compile all the `.proto` files from `/home/user/protos` into Python modules inside `/home/user/generated`. Make sure to set the correct import paths (`-I`) so the dependencies resolve correctly. Make `/home/user/generated` a valid Python package by adding an empty `__init__.py`.

3. **Serialization/Deserialization Test:**
   Write a Python script at `/home/user/test_serde.py`. This script should:
   - Import the generated modules from `/home/user/generated`.
   - Create an instance of `myproject.service.UserResponse`.
   - Set the `message` field to `"Success"`.
   - Set the nested `user.id` to `42`.
   - Set the nested `user.name` to `"Bob"`.
   - Set the nested `user.status` to the `OK` enum value defined in `base.proto`.
   - Serialize this message to binary format and write the raw bytes to `/home/user/payload.bin`.

Ensure that `python3 /home/user/test_serde.py` runs successfully and creates `/home/user/payload.bin`. Do not modify the original `.proto` files.