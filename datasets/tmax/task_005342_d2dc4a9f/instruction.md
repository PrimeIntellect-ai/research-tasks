You are a data analyst investigating a corporate network. You have been provided with a baseline dataset of communication logs, but some of the most critical communication logs were recovered as an audio dictation by a whistleblower.

Your objective is to integrate the standard data with the audio data, perform a network analysis, and extract the most influential nodes.

Here are the specific steps:
1. **Analyze the Baseline Data**: You will find a CSV file at `/home/user/data/baseline_network.csv` containing directed communication edges with columns: `source`, `target`, `weight`.
2. **Process the Audio Data**: A whistleblower dictated missing, highly sensitive network edges. This audio file is located at `/app/recovered_links.wav`. You must transcribe this audio (you may install tools like `openai-whisper` or `SpeechRecognition` via pip). The audio dictates edges in a consistent natural language format, such as: "Edge from NodeA to NodeB with weight X".
3. **Integrate and Map**: Parse the transcribed text to extract the missing edges and append them to the baseline data.
4. **Graph Analytics**: Construct a directed graph using all edges (baseline + audio-recovered). If there are multiple edges between the same source and target, sum their weights. Compute the PageRank centrality for every node in the graph. Use the standard PageRank algorithm (e.g., using `networkx`) with `alpha=0.85`, `max_iter=100`, and edge weights considered (using the `weight` attribute).
5. **Format and Export**: Export the calculated PageRank scores to `/home/user/pagerank_results.csv`. The CSV must have exactly two columns: `node` and `pagerank_score`. Sort the results in descending order by `pagerank_score`. For ties in the score, sort alphabetically by `node`. Format the `pagerank_score` to 6 decimal places.

Your final output will be evaluated programmatically. An automated script will calculate the Mean Squared Error (MSE) between your PageRank scores and the hidden ground-truth scores. Your results must achieve an MSE of strictly less than `0.00001` to pass.