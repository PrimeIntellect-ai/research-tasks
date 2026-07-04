You are a developer tasked with organizing and testing a mathematical project involving deterministic finite automata (DFA) state machines. 

Currently, there are unorganized and buggy DFA definitions in `/home/user/legacy_models/`. Your task is to organize these models, fix them using a provided patch file, build a DFA parser/simulator in Python, and write unit tests for it.

Please complete the following steps:

1. **Organize and Patch:**
   - Create a new directory called `/home/user/dfa_models/`.
   - You have a patch file at `/home/user/fixes.patch`. Apply this patch to the files in `/home/user/legacy_models/`.
   - Move all `.dfa` files from `/home/user/legacy_models/` to `/home/user/dfa_models/`.

2. **Build the State Machine Parser & Simulator:**
   - Write a Python script at `/home/user/simulator.py`.
   - The script should take two command-line arguments: the path to a `.dfa` file and a binary input string (e.g., `python3 simulator.py path/to/m1.dfa 1010`).
   - The `.dfa` files have the following format:
     ```
     STATES: <comma_separated_list_of_states>
     START: <start_state>
     ACCEPT: <comma_separated_list_of_accept_states>
     TRANSITIONS:
     <state>, <input_symbol> -> <next_state>
     ...
     ```
   - The simulator must parse this file, start at the `START` state, and process the input string character by character according to the `TRANSITIONS`.
   - If the final state after processing the entire string is in the `ACCEPT` list, print `ACCEPT` to standard output. Otherwise, print `REJECT`.
   - If a transition is missing for a given state and input symbol, the machine should immediately halt and the result is `REJECT`.

3. **Unit Testing:**
   - Write a unit test file at `/home/user/test_simulator.py` using Python's built-in `unittest` framework.
   - It must import your simulator logic and test at least one ACCEPT and one REJECT scenario.
   - Note: Do not rely solely on `subprocess` to run the tests; structure your `simulator.py` so that its parsing and simulation logic can be imported and directly tested in `test_simulator.py`.

4. **Evaluation:**
   - Run your simulator on all the `.dfa` files in `/home/user/dfa_models/` using the input string `110011`.
   - Write the results to a log file at `/home/user/evaluation.log`.
   - The format of `/home/user/evaluation.log` must be exactly:
     ```
     m1.dfa: <ACCEPT/REJECT>
     m2.dfa: <ACCEPT/REJECT>
     ```
     (Alphabetical order by filename).

Ensure all files are created exactly at the specified paths.