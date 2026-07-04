You are a release manager preparing a new deployment pipeline. The deployment logic is defined as a custom State Machine in a legacy DSL (Domain Specific Language) file that has been encoded in Base32. You need to decode the rules, parse the State Machine DSL, and build an interpreter to test various deployment scenarios.

Your task is to write a Python script `/home/user/test_runner.py` that processes the deployment scenarios and outputs the results.

### Specifications

**1. Input Files:**
- `/home/user/deploy.machine`: A Base32 encoded text file containing the state machine DSL.
- `/home/user/test_cases.json`: A JSON file containing a dictionary of test cases. Each key is a test case ID, and the value is a list of "events". Each event is a dictionary of metrics (e.g., `{"cpu_usage": 80}`).

**2. State Machine DSL Syntax:**
The decoded `deploy.machine` file will consist of state definitions and commands.
- `STATE <state_name>:` indicates the start of a state block.
- `SET <variable> = <expression>` assigns the result of an expression to a state machine variable. Variables persist across state transitions.
- `READ_EVENT` pulls the next event from the test case's event list and makes its keys available as variables. If `READ_EVENT` is executed but the event list is empty, the machine immediately halts and the final result is `TIMEOUT`.
- `IF <expression> THEN TRANSITION TO <state_name>` evaluates a boolean expression. If true, the machine immediately jumps to the target state and begins executing from the top of that state.
- `TRANSITION TO <state_name>` immediately jumps to the target state.

**3. Expressions:**
Expressions will contain integer literals, variable names, operators (`+`, `-`, `<`, `>`, `==`), and parentheses. Standard precedence rules apply. You must safely parse and evaluate these expressions. Variables used in expressions may come from previous `SET` commands or from the most recently read event.

**4. Execution Rules:**
- The machine always starts execution at the state named `START`.
- Execution halts when it transitions to a state with no commands defined (e.g., `SUCCESS` or `FAIL`), or if it hits a `TIMEOUT` via `READ_EVENT`. The name of the halting state (or `TIMEOUT`) is the final result.
- State machine variables are initialized to empty at the beginning of each test case.

**5. Output Requirement:**
Your script must evaluate all test cases in `/home/user/test_cases.json` and generate `/home/user/results.json`.
The output must be a JSON object mapping the test case ID to the final result string (e.g., `"SUCCESS"`, `"FAIL"`, or `"TIMEOUT"`).

Example Output (`/home/user/results.json`):
```json
{
  "case1": "SUCCESS",
  "case2": "FAIL",
  "case3": "TIMEOUT"
}
```

Constraints:
- Use Python 3.
- Write your own parser and evaluator; do not rely on external DSL parsing libraries (standard library only).