You are an artifact manager tasked with curating a newly ingested binary repository. 

We have a specialized, pre-vendored Python package for fast archive extraction located at `/app/fast-archive-parser` (version 1.2). This package is currently broken—it fails to install due to a deliberate configuration error in its build process. 

Your tasks:
1. **Fix and Install the Package:** Inspect `/app/fast-archive-parser`. Fix the build perturbation (hint: check the environment variables expected by its `setup.py` or `Makefile`) and install the package into your Python environment. You do not need internet access for this.
2. **Extract Archives:** You will find a nested multi-part archive at `/home/user/incoming/repository.tar.gz`. Use the fixed `fast-archive-parser` (or standard libraries if you prefer, but the package provides specialized tools) to safely extract it to a temporary directory. Handle the extraction carefully.
3. **Parse Metadata:** Inside the extracted contents, there are binary artifacts and associated `*.log` files containing multi-line log records. Each log record describes a binary artifact. Records start with `[START ARTIFACT]` and end with `[END ARTIFACT]`. Parse these multi-line logs to extract the `Artifact-ID`, `Checksum`, and `Status`.
4. **Format Conversion & Curating:** Convert this parsed configuration into a structured JSON format. Select only artifacts where `Status: VALID`. 
5. **Atomic Write:** Write the final JSON array of valid artifact metadata to `/home/user/curated_metadata.json`. You must use atomic writes (e.g., writing to a temporary file first and then renaming it) to ensure no partial data is ever visible at the destination path.

The final JSON file `/home/user/curated_metadata.json` must be a list of objects, for example:
```json
[
  {
    "Artifact-ID": "bin-7A2F",
    "Checksum": "abc123def456",
    "Status": "VALID"
  }
]
```

Your final output will be evaluated programmatically based on the accuracy (F1 score) of the extracted valid metadata compared to our hidden reference set.