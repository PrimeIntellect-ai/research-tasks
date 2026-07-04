I'm building a script utility in C to process a batch of incoming RPC requests, but my protocol buffer definitions are failing to compile due to a circular import. 

My workspace is located at `/home/user/rpc_utility`.

Here is what you need to do:

1. **Fix the Schema:**
   The protobuf files are in `/home/user/rpc_utility/schemas/`. You will find `user.proto`, `request.proto`, and `batch.proto`. There is a circular import between `user.proto` and `request.proto`. 
   To fix it, modify `request.proto` so that the `Request` message uses a scalar `int32 owner_id = 2;` instead of the `User` message type. Remove the circular import statement. Do not change the field tags or the names of other fields.

2. **Install Dependencies:**
   Install the necessary dependencies to compile Protocol Buffers to C (`protobuf-c-compiler` and `libprotobuf-c-dev`).

3. **Compile the Schemas:**
   Compile the `.proto` files into C source and header files using `protoc-c`. Place the generated `.pb-c.c` and `.pb-c.h` files in `/home/user/rpc_utility/src/`.

4. **Write the C Processor:**
   Write a C program at `/home/user/rpc_utility/src/processor.c`. 
   This program must:
   - Read a binary protobuf file located at `/home/user/rpc_utility/data/input.bin`. This file contains a serialized `RequestBatch` message.
   - Deserialize the `RequestBatch` using the generated `protobuf-c` functions.
   - Implement a custom rate-limiting data structure (e.g., a simple hash map, linked list, or array) to track the number of requests per `owner_id`.
   - Iterate through the requests in the batch in order. Validate each request against the rate limiter: a maximum of **2 requests per `owner_id`** are allowed. Any subsequent requests from the same `owner_id` in this batch should be rejected.
   - Write the `req_id` of every *allowed* request to `/home/user/rpc_utility/allowed.log`, one ID per line.

5. **Build and Run:**
   Compile your C program to an executable at `/home/user/rpc_utility/bin/processor`. Ensure it is linked properly against `protobuf-c`. Run the executable to generate the `allowed.log` file.