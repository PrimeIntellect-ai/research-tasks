You are a mobile build engineer responsible for maintaining our local CI/CD pipelines. The security team recently updated our local build proxy token and left a voicemail containing the new emergency token at `/app/voicemail.wav`.

Your task is to implement a secure, local Python HTTP server that resolves our mobile build dependency graph. 

Requirements:
1. Extract the authentication token from the audio file `/app/voicemail.wav`. The voicemail states a four-word token. Translate this into a hyphen-separated, all-uppercase string (e.g., if the recording says "alpha two charlie four", the token is `ALPHA-TWO-CHARLIE-FOUR`).
2. Write and run a Python HTTP web service listening exactly on `127.0.0.1:9000`.
3. The server must enforce an `Authorization: Bearer <TOKEN>` header for all requests. If the header is missing or incorrect, it must return an HTTP 401 Unauthorized status code.
4. The server must expose a single endpoint: `GET /build-order`.
5. When a valid request is made to `/build-order`, the server must read the JSON file `/home/user/mobile_graph.json`. This file contains a dictionary mapping mobile module names to a list of their direct dependencies.
6. The endpoint must compute a valid build order (topological sort) from the base dependencies up to the final targets. 
7. To ensure the build order is strictly deterministic, you must break ties alphabetically: when multiple modules have all their dependencies met and are ready to be built, always select the module whose name comes first alphabetically.
8. The endpoint must return an HTTP 200 OK status code with the JSON array representing this strictly ordered build list.
9. Start your server in the background (or in a way that allows the terminal to remain active) so the automated verifier can send requests to it.