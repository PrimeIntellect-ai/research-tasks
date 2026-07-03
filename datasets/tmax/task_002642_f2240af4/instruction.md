You are an AI assistant helping a data researcher organize and process a massive collection of crowdsourced knowledge graph datasets.

The researcher has left an audio note detailing the specific rules for filtering corrupted or "hallucinated" graph datasets submitted by automated scrapers. 
You need to complete a multi-stage workflow:

1. **Audio Decoding**: 
   There is an audio file located at `/app/audio/lab_notes.wav`. Transcribe this audio to understand the specific graph structural rule the researcher wants to use to separate valid graphs from invalid ("evil") ones. You may install and use any standard transcription tools (e.g., python `SpeechRecognition` + `pocketsphinx`, or whisper tools if available in the environment).

2. **Adversarial Graph Filter (C++)**:
   The researcher has provided two directories containing edge-list files (format: `node1 node2` on each line, representing directed edges):
   - `/app/corpora/clean/` (Valid knowledge graphs)
   - `/app/corpora/evil/` (Corrupted/invalid knowledge graphs)
   
   Write a C++ program at `/home/user/kg_filter.cpp` and compile it to `/home/user/kg_filter`. 
   The program must accept a single file path as a command-line argument.
   It must parse the graph and apply the structural rule mentioned in the audio recording.
   - If the graph violates the rule (is "evil"), the program MUST exit with code `1`.
   - If the graph conforms to the rule (is "clean"), the program MUST exit with code `0`.
   
   Your compiled binary will be tested against a holdout dataset of clean and evil graphs. It must achieve 100% accuracy on both.

3. **Graph Summarization**:
   For the specific clean graph located at `/app/corpora/clean/graph_001.txt`, modify your C++ program (or write a new one at `/home/user/summarize.cpp`) to compute the node with the highest total degree (in-degree + out-degree). 

4. **Final Output**:
   Create a JSON file at `/home/user/final_report.json` with the following structure:
   ```json
   {
       "audio_transcript": "<your transcription of the audio>",
       "filtering_rule": "<a 1-sentence summary of the rule from the audio>",
       "top_node_graph_001": "<node ID with highest total degree in clean/graph_001.txt>"
   }
   ```