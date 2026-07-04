You are an AI assistant helping a computational chemistry researcher automate a data pipeline. The researcher left a voice memo with specific analysis parameters, and you have a raw dataset of molecular graphs that contains both valid and malformed data.

Your goal is to orchestrate a workflow that filters the dataset, computes network graph metrics, and calculates bootstrap confidence intervals according to the researcher's audio instructions.

**Step 1: Extract Parameters**
The researcher's instructions are in an audio file located at `/app/pi_instructions.wav`. You will need to transcribe or listen to this file (e.g., using `whisper` or similar audio processing tools you can install) to find out:
- Which graph metric to calculate.
- The number of bootstrap resamples to use.
- The confidence interval percentage.

**Step 2: Adversarial Corpus Classifier**
The raw molecular graphs are stored in JSON format. The PI noted that the upstream generation process sometimes creates chemically impossible structures.
You must write a strict classifier script at `/home/user/classifier.py`.
It must take a single file path as an argument:
`python /home/user/classifier.py <path_to_json>`
- It must exit with code `0` if the graph is chemically valid (clean).
- It must exit with code `1` if the graph is invalid (evil).
A graph is considered valid if and only if it obeys these maximum valency constraints based purely on the provided edges (bonds):
- Hydrogen (H): maximum degree 1
- Oxygen (O): maximum degree 2
- Carbon (C): maximum degree 4
- Nitrogen (N): maximum degree 3

The JSON format for each file is:
```json
{
  "atoms": [{"id": 0, "element": "C"}, {"id": 1, "element": "O"}],
  "bonds": [[0, 1]]
}
```

**Step 3: Notebook Orchestration & Bootstrapping**
Create a Jupyter notebook at `/home/user/analysis.ipynb`. The notebook must:
1. Identify all "clean" JSON files in the `/app/corpus/` directory (including subdirectories) by using your `classifier.py`.
2. For each clean graph, use a graph library (like `networkx`) to calculate the specific graph metric requested in the audio file.
3. Perform a bootstrap analysis on the mean of this metric across all clean graphs. Use the exact number of resamples and confidence level specified in the audio file.
4. Output a final file at `/home/user/final_result.json` containing the bootstrap confidence bounds:
```json
{
  "metric": "<metric_name_from_audio>",
  "ci_lower": 0.123,
  "ci_upper": 0.456,
  "num_clean_graphs": 42
}
```

Ensure your `classifier.py` is robust, as it will be rigorously tested against an adversarial test suite of purely clean and purely evil molecular graphs to ensure no bad molecules slip through and no good ones are discarded.