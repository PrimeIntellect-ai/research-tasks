You are an AI assistant helping a data researcher organize a dataset of entities and their interactions.

The researcher has an audio log of field notes located at `/app/network_log.wav`. The audio contains a spoken list of undirected connections between people in a network, in the format "[Person1] knows [Person2]." 

Your task is to:
1. Transcribe the audio to extract the connections and map out the entire undirected graph. You can use standard tools available in the Linux environment (e.g., `whisper`, `ffmpeg`, or Python-based audio processing libraries). 
2. Write a Bash script at `/home/user/query.sh` that takes exactly one argument (a person's name) and outputs their exact 2-hop neighborhood based on the transcribed graph.

**2-hop neighborhood rules:**
- A node is in the 2-hop neighborhood if it is exactly two edges away from the target node.
- The 2-hop neighborhood must *exclude* the target node itself and any of its direct 1-hop neighbors.
- The output must be a single line of space-separated names, sorted alphabetically.
- If the node does not exist in the graph or has no valid 2-hop neighbors, the script must output `NONE`.

**Example:**
If the graph contains:
`Alice knows Bob.`
`Bob knows Charlie.`
`Alice knows Eve.`
`Eve knows Frank.`
`Frank knows Bob.`

Running `./query.sh Alice` should evaluate:
- 1-hop: Bob, Eve
- 2-hop via Bob: Charlie, Frank, Alice
- 2-hop via Eve: Frank, Alice
- Filter out Alice (self) and Bob, Eve (1-hop).
- Output: `Charlie Frank`

Your final script `/home/user/query.sh` must be executable and function entirely offline without external API calls. Ensure it perfectly handles the relationships defined in the audio log. An automated fuzzing verifier will run your script with various random names to ensure exact behavioral equivalence with our reference implementation.