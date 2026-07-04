You are tasked with building a pre-commit manifest filter for our Kubernetes CI/CD pipeline. Currently, invalid deployment manifests are crashing our operator. We need a Bash script that acts as a stream filter to sanitize incoming Kubernetes YAML configurations.

Additionally, a rogue pipeline monitoring process has been leaving glitchy artifacts in our video logs. You will need to analyze a captured video log of the CI/CD dashboard to extract a specific termination signal.

Here are your instructions:

1. **Video Analysis**:
   There is a video log located at `/app/k8s_dashboard.mp4`. It contains a recording of a terminal. Somewhere in this video, a specific 15-character uppercase string (the "Magic Termination Signal") flashes briefly on the screen. Use `ffmpeg` (which is pre-installed) to extract the frames, find this string, and note it down. 

2. **Build the Filter Script**:
   Create a Bash script at `/home/user/k8s_filter.sh`. This script will run as part of our CI/CD pipeline, taking raw manifest text via standard input (`stdin`) and printing the processed text to standard output (`stdout`).

   The script must apply the following transformations line-by-line:
   - If a line contains the exact substring `imagePullPolicy: Always`, replace it with `imagePullPolicy: IfNotPresent`.
   - If a line matches the regex `^ *replicas: *([0-9]+)$` (e.g., `  replicas: 10`), check the number. If the number is strictly greater than `5`, you must cap it by changing the line to exactly match the leading spaces, followed by `replicas: 5`. (e.g., `  replicas: 10` becomes `  replicas: 5`).
   - If the script encounters a line that EXACTLY matches the "Magic Termination Signal" you extracted from the video, the script must output `--- SYSTEM HALTED ---` and immediately exit with code `0`, ignoring any further input.
   - All other lines must be printed to `stdout` completely unmodified.

Ensure your script is executable and relies solely on bash built-ins or standard Unix utilities (like `sed` or `awk` if necessary, though pure Bash is preferred). Do not write output to any files; only use `stdout`.