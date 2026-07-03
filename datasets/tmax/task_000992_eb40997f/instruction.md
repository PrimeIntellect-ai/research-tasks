I have a custom C-based HTTP server for a web security project located in `/home/user/server_src`, but the project currently fails to compile due to a Makefile linking error. Additionally, the server relies on a secret passphrase for its Basic Authentication mechanism, but I've lost the documentation. Luckily, I intercepted a voicemail containing the passphrase, which is saved at `/app/intercepted_comms.wav`.

Please do the following:
1. Analyze the audio file `/app/intercepted_comms.wav` (you can use tools like `whisper` or `ffmpeg` available in the system) to extract the single-word spoken passphrase.
2. Update the `/home/user/server_src/auth.h` file and set the `SECRET_PASSPHRASE` macro to the exact word you extracted (lowercase).
3. Fix the `Makefile` in `/home/user/server_src` so that the project compiles successfully. The target `http_server` currently fails during the linking stage.
4. Run the unit tests by executing `make test` and ensure they pass.
5. Run the performance benchmark suite by executing `make bench` and save its console output to `/home/user/bench_results.txt`.
6. Start the compiled server in the background so it listens on port `8080`. You can start it via `./http_server 8080`.

Ensure the server is running and bound to `127.0.0.1:8080` so that it can be tested by our automated integration suite.