You are a data analyst tasked with computing a custom influence metric for a network dataset. 

We recently had a stakeholder meeting where the exact algorithm for this custom influence metric was defined. I have uploaded the recording of this meeting to `/app/meeting_recording.wav`. 

You also have access to the network data in `/app/edges.csv`, which contains two columns: `source` and `target`, representing directed edges in our graph.

Your task is to:
1. Transcribe or listen to `/app/meeting_recording.wav` to understand the exact mathematical rules and parameters of the custom influence metric.
2. Implement this algorithm to process the `edges.csv` dataset. You may use any language or tools you prefer. 
3. Calculate the final influence score for every node in the network based on the rules described in the audio.
4. Save your final results to `/home/user/influence_scores.csv`. The file must have exactly two columns: `node` (the node ID as a string) and `score` (the calculated score as a float). 

To succeed, your computed scores must be highly accurate compared to the reference implementation. Ensure you pay close attention to the parameters (initial values, retention rates, distribution rates, base additions, and iteration counts) mentioned in the audio.