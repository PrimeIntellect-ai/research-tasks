You are a data engineer building an automated ETL pipeline that processes workflow dependency graphs.

We receive workflow schemas exported as JSON files, where each file contains an array of edges (e.g., `[{"source": "TaskA", "target": "TaskB"}, ...]`). 

Your task is to write a standalone classifier script that identifies valid ("clean") workflows and invalid ("evil") workflows.

A workflow is considered "clean" ONLY if it meets both of the following conditions:
1. It is a strictly Directed Acyclic Graph (DAG). Any graph containing one or more cycles is "evil".
2. The maximum hierarchical execution depth (the longest path from any root node to any leaf node) is less than or equal to a strict threshold limit, `D`.

To determine the dynamic threshold limit `D`, you must analyze the reference video provided at `/app/reference.mp4`. This video is an artifact from the workflow UI system. It consists mostly of pure black frames, but flashes pure white frames (rgb: 255, 255, 255) periodically to indicate the system's current max depth configuration. The threshold `D` is exactly equal to the total number of pure white frames present in the video. You will need to extract and analyze the frames of this video to find `D`.

You must create an executable script at `/home/user/classify.py` (you may use Python, Node.js, Perl, or any pre-installed scripting language, but name the file accordingly, e.g., `.py`, `.js`, `.sh`).

The script must accept exactly two positional arguments:
1. `input_directory`: A path to a directory containing the JSON workflow files.
2. `output_csv`: A path where your script must save the classification results.

The output CSV must have the exact header `filename,status`.
Each row should contain the base filename of the JSON file and its classification (either `clean` or `evil`). 

Example expected execution:
`/home/user/classify.py /app/sample_workflows /home/user/results.csv`

Ensure your script handles standard graph traversals accurately.