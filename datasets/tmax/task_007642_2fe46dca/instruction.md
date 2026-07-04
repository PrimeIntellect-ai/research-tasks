You are a platform engineer maintaining a CI/CD pipeline. We are migrating our CI runners to a minimal Linux environment that only supports Go and no longer has Python installed. 

One of our critical pipeline steps evaluates a "pipeline health score" using a Reverse Polish Notation (RPN) mathematical expression. The expression is passed securely as a Base64 encoded string, and the dynamic metrics are provided as a JSON file.

We have an existing Python script (`/home/user/legacy_eval.py`) that successfully performs this task. Your objective is to translate this script's functionality into Go. 

Here are the requirements:
1. Create a Go program at `/home/user/evaluate.go`.
2. The program must read a Base64 encoded RPN expression from `/home/user/pipeline_data.b64`.
3. It must decode the Base64 string to get the plain text RPN expression.
4. It must read variable values from `/home/user/vars.json`. The JSON is a flat dictionary mapping string variable names to integer values.
5. It must evaluate the RPN expression using the decoded string and the variables. The supported operators are `+`, `-`, `*`, and `/` (integer division).
6. It must write the final integer result to `/home/user/result.txt`.

The legacy Python script is located at `/home/user/legacy_eval.py` for you to use as a reference for the exact evaluation logic.

Please write the Go code, compile it, and run it to produce `/home/user/result.txt`.