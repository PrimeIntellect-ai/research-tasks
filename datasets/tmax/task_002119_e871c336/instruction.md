You are tasked with fixing and completing a bash-based Kubernetes operator controller. The operator generates Pod manifests and is scheduled via a custom supervisor script, but it is currently failing due to hardcoded values, missing components, and environment/PATH inconsistencies when run as a cron-like background job.

You must complete the following steps:

1. **Extract Instructions from Voicemail**
   Listen to (transcribe) the audio file located at `/app/voicemail.wav`. The operator's primary user has left a voicemail specifying three critical configuration values:
   - The exact Timezone (TZ) to use.
   - The exact Locale (LANG) to use.
   - The absolute directory path where the operator should write its generated manifest logs.
   *Note: A local transcription tool is available at `/usr/local/bin/whisper`.*

2. **Develop the Manifest Generator (`/home/user/generate_manifest.sh`)**
   You need to write a bash script at `/home/user/generate_manifest.sh` that takes exactly three positional arguments:
   - `$1`: Pod Name
   - `$2`: Timezone
   - `$3`: Locale
   
   This script must output a Kubernetes Pod YAML manifest. We have provided a reference binary at `/app/oracle_generator`. Your bash script's standard output must be **BIT-EXACT** (character for character, including whitespace and newlines) to the output of `/app/oracle_generator "$1" "$2" "$3"`.
   You can run the oracle with test inputs to reverse-engineer the exact YAML template, indentation, and structure.

3. **Fix the Supervisor Wrapper (`/home/user/operator/cron_wrapper.sh`)**
   Create a bash script at `/home/user/operator/cron_wrapper.sh`. This script is executed by a barebones scheduling daemon with a completely empty `PATH` environment variable.
   The wrapper script must:
   - Successfully invoke your `/home/user/generate_manifest.sh` script.
   - Pass the pod name `system-logger-pod` as the first argument.
   - Pass the Timezone and Locale you extracted from the voicemail as the second and third arguments.
   - Redirect the standard output of the manifest generator to a file named `latest_manifest.yaml` inside the log directory specified in the voicemail. (You must create this directory if it does not exist).
   
Make sure `/home/user/generate_manifest.sh` and `/home/user/operator/cron_wrapper.sh` are executable. Do not use any external dependencies in `generate_manifest.sh` other than standard bash built-ins and coreutils.