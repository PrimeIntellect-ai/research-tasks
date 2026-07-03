You are acting as a database administrator. We have a graph data processing pipeline written entirely in Bash using standard Linux utilities. 

Currently, our system has a bug. A junior engineer left a voice memo detailing the issue and the requirements for the fix. The audio recording is located at `/app/bug_report.wav`. 

You have two datasets in `/app/data/`:
1. `nodes.csv` (Format: `node_id,node_type`)
2. `edges.csv` (Format: `source_id,target_id`)

The previous pipeline (which was deleted) suffered from an implicit cross join that caused out-of-memory errors. 

Your task:
1. Transcribe the audio file `/app/bug_report.wav` to understand the query requirements. You may use the pre-installed `whisper-cli` or `ffmpeg` + `whisper.cpp` tools available on the system.
2. Based on the audio's instructions, write a highly optimized Bash script at `/home/user/graph_query.sh` that performs the requested 2-hop graph traversal and node filtering using ONLY shell built-ins, `awk`, `grep`, `join`, `sort`, or `sed`. Do not use Python, Perl, or any external database engines.
3. Your script should execute the pipeline and write the output to `/home/user/result.csv`.
4. The output `/home/user/result.csv` must be a CSV with no header, containing exactly three columns: `start_node,intermediate_node,end_node`.

We will evaluate the correctness of your output using an F1-score metric against the hidden ground truth. Your output needs to achieve an F1 score of at least 0.95.