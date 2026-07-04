You are an AI assistant helping a technical writer organize a large, legacy documentation export into a modern file structure. 

The writer has an exported documentation file located at `/home/user/legacy_docs.json`. This file is currently encoded in `Windows-1252` and contains an array of article objects. 

We have a custom, proprietary Python package called `pydocorg` that parses this JSON, splits it into individual Markdown files, and organizes them by tags using symbolic links. The source code for this package is pre-vendored on your system at `/app/vendor/pydocorg-1.2.0`.

However, the pipeline is currently broken, and you need to fix it by completing the following steps:

1. **Character Encoding Conversion**: The `pydocorg` tool strictly requires `UTF-8` input, but the current export is in `Windows-1252`. Convert `/home/user/legacy_docs.json` to `UTF-8` and save it as `/home/user/docs_utf8.json`.
2. **Fix the Vendored Package**: There is a known bug in the vendored package. Specifically, the symlink generation logic in `/app/vendor/pydocorg-1.2.0/pydocorg/linker.py` creates broken or "dead" symbolic links because it uses an incorrect relative path offset when linking from the `tags` directory to the `articles` directory. Inspect the package, identify the bug, and patch `linker.py`. 
3. **Run the Pipeline**: Once the bug is fixed, install the package (e.g., using `pip install -e /app/vendor/pydocorg-1.2.0`) and run its CLI tool on the converted file:
   `pydocorg build --input /home/user/docs_utf8.json --output /home/user/dist`

The final output in `/home/user/dist` should contain an `articles/` directory with the generated Markdown files, and a `tags/` directory containing symbolic links that correctly point back to the actual Markdown files in the `articles/` directory.

Our automated testing suite will evaluate your success by calculating a "Symlink Validity Metric" based on the percentage of correctly resolving symbolic links in the `/home/user/dist/tags` directory.