You are helping a development team migrate an old Python 2 web service to a new C++ microservice architecture using gRPC. As part of this migration, the URL routing definitions need to be translated into Protobuf service definitions.

Your task consists of the following steps:

1. **Patch the routing file**: 
   In `/home/user/workspace`, there is a file named `routes.txt` containing the legacy Python 2 route definitions. There is also a patch file named `py3_migration.patch` in the same directory. This patch updates the route definitions to our new standard (it removes deprecated endpoints and adds some new ones).
   Apply `py3_migration.patch` to `routes.txt`.

2. **Write a C++ Code Generator**:
   Write a C++17 program at `/home/user/workspace/generate_proto.cpp` that reads the patched `routes.txt` file and generates a valid Protobuf v3 file at `/home/user/workspace/api.proto`.

   The `routes.txt` file format (after patching) contains one route per line in the format:
   `[HTTP_METHOD] [URL_PATTERN] [RPC_METHOD_NAME]`
   
   The URL pattern may contain path parameters enclosed in angle brackets, formatted as `<type:parameter_name>`. The valid types are `int` (which maps to Protobuf `int32`) and `str` (which maps to Protobuf `string`).

3. **Protobuf Generation Rules**:
   Your C++ program must generate an `api.proto` file with the following exact structure:
   - Uses `proto3` syntax.
   - Declares the package `api`.
   - Defines a service named `ApiService`.
   - For each route in `routes.txt`, add an RPC to `ApiService` named `[RPC_METHOD_NAME]`. It takes a request message named `[RPC_METHOD_NAME]Request` and returns a response message named `[RPC_METHOD_NAME]Response`.
   - For each RPC, define the corresponding request and response messages.
   - The Request message must contain fields for each path parameter found in the URL pattern, matching the parameter's name and mapped type. Assign field numbers sequentially starting from 1 in the order they appear in the URL.
   - The Response message should be empty.

   *Example Input Route:*
   `POST /user/<int:user_id>/document/<str:doc_id> UploadDocument`

   *Example Output Protobuf:*
   ```protobuf
   syntax = "proto3";
   package api;

   service ApiService {
     rpc UploadDocument(UploadDocumentRequest) returns (UploadDocumentResponse);
   }

   message UploadDocumentRequest {
     int32 user_id = 1;
     string doc_id = 2;
   }

   message UploadDocumentResponse {
   }
   ```
   *(Ensure proper formatting, with 2 spaces for indentation inside blocks. The order of RPCs and messages in the proto file should match the order of routes in `routes.txt`.)*

4. **Execute**:
   Compile your C++ program using `g++ -std=c++17 generate_proto.cpp -o generate_proto` and run it. Ensure `/home/user/workspace/api.proto` is created successfully.