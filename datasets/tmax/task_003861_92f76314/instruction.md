You are an artifact manager tasked with curating a binary repository. Our ingestion system has dumped several artifacts, metadata, and logs into the `/home/user/workspace/` directory, but the data is unorganized, and some of the ingested artifacts are corrupted or failed ingestion. 

Your objective is to write and execute a Python script to process this data, filter out invalid artifacts, and build a curated, space-efficient directory structure.

Here are the details of the input data located in `/home/user/workspace/`:
1. **`/home/user/workspace/artifacts/`**: A directory containing `.zip` artifact files.
2. **`/home/user/workspace/repo_index.json`**: A JSON file mapping an internal `Artifact-ID` to its metadata (project, version, filename).
3. **`/home/user/workspace/ingest.log`**: A multi-line log file detailing the ingestion process. Each log record spans multiple lines enclosed by `[START]` and `[END]` markers. Example:
   ```
   [START]
   Date: 2023-10-25
   Artifact-ID: ART-001
   Status: SUCCESS
   Message: Ingested successfully.
   [END]
   ```

Your task has the following requirements:

**Phase 1: Parsing and Filtering**
- Parse the multi-line log `ingest.log`. Identify the `Artifact-ID` and its `Status` for each record. 
- You must ONLY process artifacts whose status is `SUCCESS` or `WARNING`. Completely ignore artifacts with a `FAILED` status.
- Cross-reference the valid `Artifact-ID`s with `repo_index.json` to get the `filename`, `project`, and `version`.
- Verify the integrity of the corresponding `.zip` archive in `/home/user/workspace/artifacts/`. Some ZIP files may be corrupted. If a ZIP file fails integrity checks (e.g., using `zipfile` module or `unzip -t`), skip it.

**Phase 2: Curated Repository Creation**
For all artifacts that passed the status and integrity checks:
- Create a curated directory structure under `/home/user/workspace/curated/` with the format: `/home/user/workspace/curated/<project>/<version>/`
- To save disk space, **hard link** the valid original `.zip` artifact into its corresponding new `<project>/<version>/` directory.
- For each `<project>` in the curated directory, create a **symbolic link** named `latest` (i.e., `/home/user/workspace/curated/<project>/latest`) that points to the directory of its highest semantic version. You can assume versions are in the format `X.Y.Z` and can be sorted using standard semantic versioning rules.

**Phase 3: Summary Report**
- Generate a summary CSV report at `/home/user/workspace/curated_summary.csv`.
- The CSV must have the following headers exactly: `Project,Version,Filename,Status`
- Ensure the CSV only contains rows for artifacts that successfully made it into the curated repository (passed both log status and zip integrity). Sort the CSV alphabetically by `Project`, then by `Version` in descending order.

You may install any required python packages. You may run bash commands alongside your Python scripts.