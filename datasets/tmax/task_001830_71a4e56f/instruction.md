You are a build engineer responsible for managing our new artifact processing pipeline. We have a Rust-based tool that resolves dependency graphs of build artifacts, processes them, and outputs a final metadata manifest.

However, the tool is currently broken and incomplete. Your task is to fix and finalize it.

The source code is located at `/home/user/artifact_manager`. 

Here is what you need to do:
1. **Fix Rust Ownership and Graph Traversal**: The current code attempts to perform a topological sort of the build artifacts parsed from `/home/user/artifact_manager/artifacts_graph.json`, but it fails to compile due to borrow checker errors and incorrect custom data structure usage in `src/graph.rs` and `src/main.rs`. Fix the compiler errors so that it correctly traverses the graph from roots to leaves.
2. **Implement Serialization**: Ensure the final sorted artifacts are correctly serialized back to JSON. You will need to implement the appropriate Serde traits.
3. **Process Audio Artifacts**: The graph contains an artifact of type `"audio_memo"` located at `/app/artifacts/release_notes_v2.wav`. Our pipeline requires converting this audio artifact into text. Integrate a step in the Rust program (or call an external script/tool from it) to transcribe this audio file. You may install and use external transcription tools like Python's `openai-whisper` or `SpeechRecognition` to accomplish this. 
4. **Output Constraint**: The final output must be written to `/home/user/final_artifacts.json`. It must be a JSON array of objects, topologically sorted (dependencies before the items that depend on them). For the audio artifact, the JSON object must include a field called `"transcription"` containing the transcribed text.

Example expected output format for `/home/user/final_artifacts.json`:
```json
[
  {
    "id": "base_lib",
    "type": "binary"
  },
  {
    "id": "release_notes",
    "type": "audio_memo",
    "transcription": "the text of the audio memo goes here"
  }
]
```

To complete this task, modify the Rust code, successfully compile it, run it against the provided `artifacts_graph.json`, and generate the valid `/home/user/final_artifacts.json` file with the transcribed audio.