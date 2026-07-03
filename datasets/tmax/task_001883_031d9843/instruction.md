You are a systems programmer migrating an older C-based sensor processing pipeline to a modern Python gRPC service. Unfortunately, we lost the original C header file that defines the primary data structure, but we managed to find a screenshot of the code snippet containing the struct definition.

The image is located at `/app/struct.png`. 

Your task is to:
1. Extract the text from the image (e.g., using `tesseract` which is pre-installed).
2. Write a Python script at `/app/generate_proto.py` that reads the extracted C struct and performs a schema migration by generating a valid Protobuf 3 schema file.
3. The generated schema must be saved to `/app/sensor.proto`.

The Protobuf schema (`/app/sensor.proto`) must:
- Use `syntax = "proto3";`
- Define a `message` with the exact same name as the C struct.
- Map the C fields to their equivalent proto3 types (e.g., `int32_t` -> `int32`, `float` -> `float`, `double` -> `double`, `char array` -> `string`).
- Number the fields sequentially starting from 1, matching the order in the C struct.

The evaluation will measure the similarity of your generated `/app/sensor.proto` to our reference schema using a sequence matching metric. You do not need to compile the protobuf, just generate the accurate `.proto` text file.