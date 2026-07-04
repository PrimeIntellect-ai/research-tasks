You are a mobile build engineer maintaining a legacy asset pipeline. We need to rebuild a missing metadata encoder tool written in Go that processes asset identifiers.

The former engineer left a voice memo detailing the exact encoding rules for the asset identifiers. You can find this audio file at `/app/voice_memo.wav`. You will need to transcribe or listen to this file to understand how to transform the input strings.

Your task:
1. Define a Protocol Buffers schema at `/home/user/metadata.proto` with:
   - syntax = "proto3";
   - A package name of your choice, but specify `option go_package = "./pb";`.
   - A message named `AssetInfo`.
   - Field 1: `string data` (this will hold the encoded string).
   - Field 2: `int32 original_length` (this will hold the length of the string before encoding).

2. Generate the Go code for this protobuf schema.

3. Write a Go program at `/home/user/main.go` that does the following:
   - Reads all data from standard input (`stdin`) until EOF.
   - Trims any trailing newline character (`\n`) from the input.
   - Applies the string transformation rules specified in the `/app/voice_memo.wav` audio file.
   - Populates the `AssetInfo` protobuf message with the transformed string and the length of the original input string (after trimming the newline).
   - Serializes the message and writes the raw protobuf bytes directly to standard output (`stdout`).

4. Build your Go program and output the executable to `/home/user/encoder`.

Note: Ensure your Go environment is properly initialized (e.g., `go mod init encoder`, `go get google.golang.org/protobuf/...`). Do not print any debug information to stdout; standard output must contain strictly the serialized protobuf bytes.