A previous developer left a messy, broken polyglot video processing project in `/home/user/videoproc`. The project consists of a Python orchestrator, a Go frame-analysis service, and a C++ frame-extraction tool. Your objective is to fix the build system, organize the dependencies, and complete the Python pipeline to process a provided video file.

1. **Resolve the Go Circular Dependency & Build**:
   The Go service in `/home/user/videoproc/analyzer` fails to build because of a circular import between the `graph` package and the `models` package. Refactor the Go code to break this circular dependency without changing the core analysis logic. Once fixed, compile the Go binary to `/home/user/bin/analyzer`.

2. **Polyglot Build Orchestration**:
   Compile the C++ utility located at `/home/user/videoproc/extractor`. This tool relies on standard libraries. Output the executable to `/home/user/bin/extractor`.

3. **Graph Traversal File Organization**:
   The directory `/home/user/videoproc/assets` contains a flat list of configuration files. Write a Python script `/home/user/videoproc/organize.py` that reads `dependencies.json` (which defines a DAG of asset dependencies) and copies the files into `/home/user/videoproc/organized_assets/` such that the directory structure reflects the resolved dependency graph (e.g., `root/child/grandchild.conf`).

4. **Python WebSocket Pipeline**:
   The main task is to implement the Python orchestrator in `/home/user/videoproc/pipeline.py`. 
   - It must spawn the Go `analyzer` binary (which starts a WebSocket server on `ws://localhost:8080`).
   - It must use the C++ `extractor` binary to extract the first 100 frames from the video file located at `/app/input.mp4`.
   - It must stream these frames (as base64 encoded strings) via WebSockets to the Go analyzer.
   - The Go analyzer will return a numerical "motion score" for each frame.
   - The Python script must aggregate these scores and save them as a JSON array of floats to `/home/user/output_metrics.json`.

Ensure your pipeline completes successfully and generates the `/home/user/output_metrics.json` file. The accuracy of your motion scores will be evaluated against a reference implementation.