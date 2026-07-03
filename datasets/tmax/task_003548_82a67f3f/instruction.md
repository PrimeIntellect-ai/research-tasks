You are an artifact manager tasked with curating a legacy binary repository. The repository contains a batch of compressed artifacts that need to be normalized, converted, and cataloged. 

Currently, the artifacts are stored in `/app/legacy_repo/`. Each artifact is a `.tar.gz` file containing a binary payload and a `metadata.txt` file. 
However, the repository is messy:
1. The artifacts need to be bulk-renamed according to the mappings defined in `/app/repo_config.ini`.
2. The `metadata.txt` files inside the archives are encoded in `ISO-8859-1` and contain legacy macro-templates (e.g., strings like `__AUTHOR__` that need to be replaced by actual values).
3. We rely on a vendored utility called `shyaml` (a Python-based YAML/JSON parser used heavily in our Bash pipelines) located in `/app/shyaml-0.6.2/`. However, this package has a broken setup/source due to a recent bad commit, preventing it from running. 

Your tasks:
1. **Fix the vendored package**: Inspect `/app/shyaml-0.6.2/`, find the deliberate syntax error or broken setup, fix it, and install it locally so you can use `shyaml` in your scripts.
2. **Curate the archives**: Write a Bash pipeline that processes each `.tar.gz` file in `/app/legacy_repo/`. For each archive:
   - Identify its new name from `/app/repo_config.ini` and rename the archive.
   - Stream-process or temporarily extract the archive to read `metadata.txt`.
   - Convert the character encoding of `metadata.txt` from `ISO-8859-1` to `UTF-8`.
   - Apply a text substitution macro: replace all instances of `__STATUS__` with `CURATED`.
   - Update the `.tar.gz` with the modified `metadata.txt` (keeping the binary files intact).
3. **Generate a Catalog**: Using your fixed `shyaml` tool and Bash, parse the extracted metadata and generate a single summary file at `/home/user/manifest.json`. This file must be a valid JSON array of objects containing the new artifact name and its parsed metadata.

**Evaluation:**
Your final output will be evaluated automatically. An automated verifier will compute an accuracy score (0.0 to 1.0) by comparing the key-value pairs in your `/home/user/manifest.json` against a hidden ground-truth manifest. You must achieve a metadata extraction accuracy score of `>= 0.95`.