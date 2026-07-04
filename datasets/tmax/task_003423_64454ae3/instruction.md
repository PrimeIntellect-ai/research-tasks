We are migrating an old legacy logging system that was originally written in Python 2. In Python 2, strings were essentially raw byte arrays, and the legacy system stored log messages encoded in ISO-8859-1 (Latin-1). Our new modern infrastructure uses Python 3 and C++ connected via gRPC, which strictly requires valid UTF-8 for strings.

Unfortunately, the original `.proto` schema file for the legacy Python 2 system was lost, but we found a screenshot of the schema snippet.

Your task is to build a C++ data migration tool that reads the old legacy format and outputs the new modern format.

Here are the steps you must follow:

1. **Recover the Legacy Schema:**
   Examine the screenshot located at `/app/legacy_schema.png`. Use OCR (e.g., `tesseract`) to extract the exact `proto2` message definition for the old log format.

2. **Define the New Schema:**
   Create a new protobuf schema named `modern.proto` with `syntax = "proto3";`. It must contain the following message definition:
   ```protobuf
   message ModernLog {
     int32 log_id = 1;
     string utf8_message = 2;
   }
   ```

3. **Build the C++ Migration Tool:**
   Write a C++ program that:
   - Reads a raw binary serialized message of the legacy format from standard input (`stdin`).
   - Parses it using the recovered legacy protobuf schema.
   - Migrates the data to the new `ModernLog` protobuf message. 
   - During migration, it must map the legacy ID field to `log_id`, and convert the legacy Python 2 message bytes (which are ISO-8859-1 encoded) into valid UTF-8 before storing it in `utf8_message`.
   - Serializes the resulting `ModernLog` to standard output (`stdout`) in binary format.

4. **Compile the Tool:**
   Compile your C++ program and produce a standalone executable binary located exactly at `/home/user/migrator`. Make sure to link against the required protobuf libraries.

The automated verification system will fuzz your `/home/user/migrator` binary with thousands of randomly generated legacy payloads and ensure the outputs match a reference implementation byte-for-byte.