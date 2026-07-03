You are an integration developer responsible for testing a new mathematical API. 

The core calculation engine is written in Rust for performance, and it is exposed via a Python WebSocket server using C bindings (FFI). We have a testing client that needs to request a mathematical computation from the server.

However, the current codebase in `/home/user/math_integration` has a few issues that prevent successful integration:

1. **Rust Engine Compilation**: The Rust library located in `/home/user/math_integration/rust_engine` fails to compile due to a strict ownership/borrow checker error. You need to debug and fix `src/lib.rs` so it compiles successfully using `cargo build`.
2. **Semantic Versioning Bug**: The Python server (`/home/user/math_integration/server.py`) expects clients to use protocol version `>= 2.1.0`. It currently contains a bug where it performs a naive string comparison for versions. As a result, when a client connects with version `"10.0.0"`, the server wrongly rejects it. Fix this bug so it properly compares semantic versions.
3. **FFI Integration**: Ensure `server.py` correctly loads the compiled Rust shared library (`librust_engine.so`).
4. **Client Implementation**: Complete the client script `/home/user/math_integration/test_client.py`. It must connect to the WebSocket server at `ws://localhost:8765`, send a JSON payload requesting the calculation for `n = 20` using protocol version `"10.0.0"`, receive the integer response, and write *only* the final integer result to a file located at `/home/user/result.txt`.

**Payload Format required by the server:**
```json
{
    "version": "10.0.0",
    "n": 20
}
```

**Task Requirements:**
- Fix the Rust borrow checker bug and compile the engine.
- Fix the semantic version comparison in `server.py` and start the server in the background.
- Implement the WebSocket client in `test_client.py`.
- Run your client to fetch the result and save it to `/home/user/result.txt`.

Do not change the mathematical logic in the Rust engine; only fix the compilation error.