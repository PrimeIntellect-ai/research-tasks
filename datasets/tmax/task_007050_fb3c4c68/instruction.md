You are a platform engineer maintaining a custom CI/CD pipeline system. Our old system used a tiny, proprietary scripting language (a Domain Specific Language) to define CI pipelines, which serialized the execution commands in base64 to avoid special character escaping issues. We are migrating to a modern gRPC/Protobuf-based architecture.

Your task is to bridge the old and new systems by writing a Protobuf schema and a Bash interpreter that parses the old DSL and generates a valid Protobuf text message.

1. Create a Protobuf schema file at `/home/user/ci.proto` with `proto3` syntax. It must define:
   - A `Step` message containing two string fields: `name` (field number 1) and `command` (field number 2).
   - A `Pipeline` message containing a string field `id` (field number 1) and a repeated `Step` field named `steps` (field number 2).

2. We have a DSL file located at `/home/user/pipeline.dsl`. The DSL has two opcodes:
   - `PID <pipeline_id>`: Sets the ID of the pipeline.
   - `STP <step_name> | <base64_encoded_command>`: Adds a step with the given name and a base64-encoded bash command.

3. Write a Bash script at `/home/user/generate_proto.sh` that:
   - Reads `/home/user/pipeline.dsl`.
   - Acts as an interpreter for this DSL, extracting the pipeline ID and deserializing (base64 decoding) the commands.
   - Generates a strictly valid Protobuf text format file at `/home/user/pipeline.textproto` conforming to the `Pipeline` message defined in your `ci.proto`.
   - Ensure your script correctly escapes quotes in the decoded commands if necessary for the textproto format, though you can assume the decoded commands in our test cases will only contain simple double quotes that can be escaped as `\"`.

Make sure `/home/user/generate_proto.sh` is executable. You can use the `protoc` command-line tool (which is installed on the system) to verify your generated textproto if you wish.