I need you to complete a critical stage in our legacy Python 2 to Python 3 migration project. Our automated refactoring pipeline evaluates dynamic expressions heavily tied to our database schema, but we've lost the exact target schema version number. 

Here is what you need to do:

1. **Video Analysis (Constraint Extraction)**
We have a recording of the legacy test suite running, located at `/app/legacy_tests.mp4`. The target schema version corresponds to the exact number of completely red frames (where the entire frame is pure red) in this video. Use `ffmpeg` and Python or Bash to extract the frames and count the red frames. Save this integer count to `/home/user/schema_version.txt`.

2. **Migrator & Sanitizer Implementation**
Write a Python 3 CLI tool at `/home/user/migrator.py` that parses legacy Python 2 expressions and safely transpiles them to Python 3, applying the schema version constraint.
- The tool must take two arguments: the input file containing a legacy expression, and the output file. 
- Example invocation: `python3 /home/user/migrator.py <input_file> <output_file>`
- The tool must read the Python 2 expression (e.g., uses of `xrange`, `print "..."`, or old dictionary methods like `iteritems`) and rewrite them to their Python 3 equivalents.
- Crucially, it must parse the expression's AST to ensure it is strictly a mathematical/logical expression or basic print statement. 

3. **Adversarial Corpus Verification**
You must ensure your tool is secure against malicious injections. The directory `/app/corpus/evil/` contains files with Python snippets attempting code injection (e.g., using `eval()`, `exec`, `os.system`, or `__import__`). The directory `/app/corpus/clean/` contains valid legacy expressions that must be migrated.
- Your tool must exit with code `0` and write the migrated Python 3 code to the output file if the input is safe.
- Your tool must exit with code `1` and leave the output file empty (or untouched) if it detects malicious/unsafe operations (anything not in a very restricted safe list of nodes like BinOp, Num, Str, Print, Call to safe math functions).
- To pass, 100% of the clean corpus must be successfully migrated to valid Python 3, and 100% of the evil corpus must be rejected (exit code 1).

Please create the script, verify it against the corpora, and ensure your final code is robust.