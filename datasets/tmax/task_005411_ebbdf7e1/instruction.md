You are an AI assistant helping a wildlife researcher organize an ecosystem dataset. The researcher has recorded field observations in an audio log and needs to build a fast, local network service to query the resulting biological network (a directed graph of "eats" relationships).

Your task has three phases:

1. **Audio Processing**: 
   The researcher has left a voice recording of their field notes at `/app/ecosystem_log.wav`. 
   Use available transcription tools (e.g., `whisper` or Python libraries if you prefer to write a quick script) to transcribe this audio. The audio contains a series of observations about which animal eats which organism (e.g., "AnimalA eats AnimalB").

2. **Graph Construction & Server Implementation (C++)**:
   Write a C++ program located at `/home/user/ecosystem_server.cpp`. This program must:
   - Read the transcribed relationships and build an in-memory directed graph. 
   - Start a raw TCP server listening on `127.0.0.1:8080`.
   
3. **Query Protocol**:
   The C++ TCP server must implement a custom graph querying protocol. For every incoming connection, it should process lines of text ending in `\n`.
   - **Authentication**: The first line sent by the client MUST be exactly `AUTH: ecoweb2024`. If the auth is missing or incorrect, the server should immediately drop the connection.
   - **Querying**: After authentication, the client will send commands in the format `MATCH <NodeName>`.
   - **Response**: The server must reply with a comma-separated list of all nodes that the requested node eats (out-edges), sorted alphabetically, followed by a newline `\n`. If the node eats nothing or doesn't exist, return `NONE\n`.
   - **Persistence**: The server must keep the connection open to accept multiple `MATCH` commands until the client disconnects.

Compile your C++ program using `g++ /home/user/ecosystem_server.cpp -o /home/user/server -pthread` and run it in the background. Leave the server running so our automated verifier can connect to `127.0.0.1:8080` and run a series of integration tests against your dataset.

Write your transcription to `/home/user/transcript.txt` so you can verify it, but the primary verification will be done via the network socket.