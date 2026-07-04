I need you to help me migrate a critical legacy audio processing pipeline from Python 2 to Python 3. 

In `/home/user/legacy/audio_graph_server.py`, there is an old Python 2 script. This script acts as a WebSocket server that receives a directed acyclic graph (DAG) of audio analysis tasks in JSON format, resolves the dependency execution order, and executes them against a local audio file to extract specific metrics (e.g., peak amplitude, duration, zero-crossing rate). 

Here is what you need to do:
1. Translate and rewrite this script into modern Python 3. Save your executable script at `/home/user/py3_audio_processor.py`.
2. Instead of running as a WebSocket server for this iteration, I need the script to be a CLI tool that takes two arguments: 
   - `--audio`: the path to the audio file.
   - `--graph`: a JSON string representing the DAG of tasks.
   The tool must output the final JSON result to `stdout` and exit.
3. The graph JSON will look like this: `[{"id": "task1", "op": "duration", "deps": []}, {"id": "task2", "op": "peak", "deps": ["task1"]}]`. Your script must parse this, traverse the graph resolving dependencies correctly, perform the operations on the audio file, and output a JSON dictionary mapping task IDs to their results.
4. You must test your script against the provided audio fixture located at `/app/interview.wav`.
5. Your output must exactly match the behavior of our verified, compiled reference binary located at `/app/oracle_audio_graph`. This binary takes the exact same arguments (`--audio` and `--graph`) and produces the canonical output.

Make sure your Python 3 script is well-tested, handles the graph traversal deterministically (sorting task execution by ID when dependencies are tied), and outputs valid, compact JSON to stdout.