You are an AI assistant acting as a senior developer. 

A junior developer on your team has been writing a custom build script that parses module configuration files, resolves a dependency graph, and queries an SQLite database to assign "active" owners to the resolved modules. 

However, the build script at `/home/user/pipeline/build.py` is failing to generate the correct output. The developer reported the following symptoms:
1. Running `python3 build.py` seems to hang indefinitely (likely an infinite loop or recursion issue in the dependency resolver).
2. When the infinite loop is bypassed, the script crashes due to a format parsing error. Our configuration files use a custom `key: value` format, but there seems to be an edge case the parser isn't handling.
3. Once it runs to completion, the generated output file assigns incorrect (stale) owners to some modules. The query result debugging is needed because it should only fetch the *active* owner for each module.

Your task is to debug and fix the Python code in the `/home/user/pipeline` directory. 
- You may modify `parser.py`, `resolver.py`, `db_utils.py`, and `build.py` as needed.
- **Do not** modify `config.txt` or `metadata.db`. The data and config are perfectly valid; the bugs are in the Python logic.

When you have successfully fixed the pipeline, running `python3 build.py` from the `/home/user/pipeline` directory should exit cleanly and produce a file named `build_report.json` with the correctly resolved dependencies and active owners. 

Verify your work by ensuring `build_report.json` is generated with the accurate metadata.