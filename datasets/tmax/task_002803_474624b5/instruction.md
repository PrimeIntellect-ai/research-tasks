You are an automation specialist working on a data pipeline that streams large JSON-lines files, reshapes them from wide to long format, and generates templated text reports.

We have a vendored package located at `/app/bash-json-reshaper-1.1` which provides a fast Bash and Awk based streaming tool (`reshape.sh`) to flatten JSON-lines metrics. 
However, it currently fails or mangles data when it encounters JSON lines containing unicode escape sequences (e.g., `\u00A0` or `\u2022`) in text fields. 

Your task:
1. Identify and fix the deliberate perturbation in the vendored package `/app/bash-json-reshaper-1.1` that causes it to fail on unicode escape sequences. (Hint: look at how its configuration or environment is set up in its configuration file).
2. Write a Bash script at `/home/user/run_pipeline.sh` that acts as the primary orchestrator. 
3. `/home/user/run_pipeline.sh` must read JSON-lines from STDIN.
4. It must stream the data through the fixed `/app/bash-json-reshaper-1.1/reshape.sh` tool.
5. For each flattened record output by the reshaper, your script must generate a line of text using the following template:
   `[<id>] Metric <metric_name> has value <metric_value>. Note: <text>`
6. The output must be written to STDOUT.
7. Make sure your script handles large files efficiently by streaming the data (no loading the entire file into memory).
8. Ensure `/home/user/run_pipeline.sh` is executable.

The input JSON-lines will look like this:
`{"id": "doc_1", "metrics": {"alpha": 10, "beta": 20}, "text": "Data point\\u2022"}`

The reshaper outputs tab-separated values: `id`, `metric_name`, `metric_value`, `text`.
Your final script's output for the above line should be:
`[doc_1] Metric alpha has value 10. Note: Data point•`
`[doc_1] Metric beta has value 20. Note: Data point•`

The automated verifier will aggressively fuzz your script with thousands of random inputs and assert bit-exact equivalence against a reference implementation.