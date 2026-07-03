You are a web developer working on a backend audio processing feature. We are building a Rust-based gRPC service that extracts text from audio files using a proprietary C library, and then applies a set of standard corrections via a patch file.

Your task is to fix the existing codebase, compile it, and process a test audio file. 

Here is the current state of the system:
- A Rust project is located at `/home/user/transcription_service/`.
- The project defines a gRPC service using `tonic` (protobuf definition at `/home/user/transcription_service/proto/transcriber.proto`).
- The service uses FFI to interact with a C shared library (`libaudioprocessor.so`, installed in `/usr/local/lib/`, header at `/usr/local/include/audioprocessor.h`).
- There is a target audio file at `/app/sample.wav`.
- There is a patch file containing text corrections at `/app/corrections.patch`.

However, the previous developer left the Rust codebase in a broken state:
1. **FFI & Ownership:** The FFI bindings in `src/ffi.rs` have memory leaks and borrow checker errors regarding C-string handling and pointer lifecycles.
2. **Build System:** The `build.rs` script is not correctly linking the shared library, causing symbol resolution errors.
3. **gRPC State:** The gRPC service handler in `src/main.rs` fails to compile due to incorrect shared state management across async threads.

Your objectives:
1. Fix the Rust compiler errors, including ownership, borrow checker, and FFI issues.
2. Correct the build system to properly link `libaudioprocessor.so`.
3. Start the gRPC server.
4. Send a gRPC request to the running server to transcribe `/app/sample.wav`.
5. The server will return a raw transcript. You must apply the unified diff located at `/app/corrections.patch` to this raw transcript.
6. Save the final, patched transcript to `/home/user/final_transcript.txt`.

We will evaluate the quality of your final transcript programmatically. The Levenshtein distance between your output in `/home/user/final_transcript.txt` and the hidden ground-truth transcript must be less than or equal to 5. 

You may use any standard CLI tools (like `curl`, `grpcurl`, `patch`, etc.) alongside `cargo`. Ensure your final text file contains only the transcript content with no extraneous logging.