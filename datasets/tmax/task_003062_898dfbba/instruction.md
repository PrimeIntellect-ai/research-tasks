You are tasked with migrating a mathematical Directed Acyclic Graph (DAG) evaluator from Python 2 to a modern Python 3 REST API, and orchestrating an end-to-end multi-language test. 

Currently, there is a legacy script `/home/user/legacy_dag.py` that processes a mathematical compute graph. However, it is written in Python 2, relies on Python 2 specific syntax (like `print` statements without parentheses and `dict.iteritems()`), and is strictly a CLI tool. 

Your objectives are:
1. **Migrate and Wrap in an API**: Create a new Python 3 application at `/home/user/app.py`. It must contain the logic from `legacy_dag.py` (fixed to run in Python 3) but exposed as a REST API using `Flask` or `FastAPI`. The API must listen on `127.0.0.1:5000` and expose a `POST` endpoint at `/api/v1/compute`. 
   - The endpoint should accept a JSON body containing the graph.
   - It should return a JSON response in the format: `{"result": <evaluated_target_value>}`.

2. **End-to-End Orchestration in Ruby**: Write a Ruby script at `/home/user/test_e2e.rb` that acts as an integration test and performance benchmark. The script must:
   - Send an HTTP POST request to `http://127.0.0.1:5000/api/v1/compute` with the following JSON payload:
     ```json
     {
       "nodes": {
         "A": {"type": "value", "value": 7},
         "B": {"type": "value", "value": 3},
         "C": {"type": "add", "inputs": ["A", "B"]},
         "D": {"type": "mul", "inputs": ["C", "A"]},
         "E": {"type": "add", "inputs": ["D", "B"]}
       },
       "target": "E"
     }
     ```
   - Record the HTTP status code and parse the returned JSON.
   - Write the outcome to `/home/user/integration_result.log` exactly in this format:
     `Result: <value>, Status: <code>`

To complete the task:
- Start the Python API in the background.
- Run your Ruby end-to-end test script.
- Ensure the log file is generated successfully.