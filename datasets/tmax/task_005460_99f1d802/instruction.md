You are tasked with fixing a broken Rust project located in `/home/user/api-gateway`. The project implements a REST to gRPC gateway, but it currently fails to compile and lacks proper testing. 

Your objective is to write a single Bash script at `/home/user/fix_and_test.sh` that performs the following steps to fix the build, compile the project, and run a property-based test.

1. **Fix Protobuf Schema**: The gRPC schema at `/home/user/api-gateway/proto/service.proto` has a syntax error. It incorrectly uses the type `integer` for the `id` field. Use `sed` in your script to change `integer` to `int32`.
2. **Create build.rs**: The project is missing its `build.rs` file, which is required by `tonic-build` to compile the protobuf definitions. Your script must generate a `/home/user/api-gateway/build.rs` file with the following Rust code:
   ```rust
   fn main() -> Result<(), Box<dyn std::error::Error>> {
       tonic_build::compile_protos("proto/service.proto")?;
       Ok(())
   }
   ```
3. **Fix Rust Code**: In `/home/user/api-gateway/src/main.rs`, there is a typo in the REST handler where it attempts to call a non-existent function `fetch_record`. It should be `get_record`. Use `sed` to fix this typo.
4. **Compile**: Your script should run `cargo build --manifest-path /home/user/api-gateway/Cargo.toml`.
5. **Property-based Testing (Fuzzer)**: After a successful build, your script must start the compiled binary (`/home/user/api-gateway/target/debug/api-gateway`) in the background. Wait 2 seconds for it to start on port `8080`.
   Then, write a loop in your script that acts as a simple property-based test: it should send 50 `POST` requests to `http://localhost:8080/api/record` using `curl`. The payload must be JSON in the format `{"id": <random_number>}`, where `<random_number>` is a randomly generated integer between 1 and 10000 (using bash's `$RANDOM`).
6. **Logging**: Count the number of HTTP 200 OK responses returned by your 50 `curl` requests. Write this count to `/home/user/test_results.log` in the format `Successful requests: <count>`. Finally, kill the background Rust server process.

Ensure your script is executable and handles errors gracefully. You do not need to run the script yourself; we will execute `/home/user/fix_and_test.sh` to verify your solution.