You are tasked with building a robust configuration management pipeline in C++ that processes configuration changes from a visual audit log and sanitizes the output. 

**Stage 1: Visual Audit Log Extraction**
We have an audit video file located at `/app/audit_log.mp4`. This video encodes a sequence of configuration deployment events. 
- Use `ffmpeg` to extract the frames at 1 frame per second. 
- Write a bash or C++ script to analyze the frames. A frame is considered a "deployment event" if its top-left 10x10 pixel region is purely white (RGB 255, 255, 255). 
- Count the total number of deployment events and their frame indices (0-indexed). Save these indices to `/home/user/event_indices.txt`, one per line.

**Stage 2: Template-based DAG Orchestration**
Using the sequence of frame indices, map them to configuration nodes in `/app/config_dag.tsv`. 
- Resolve the dependencies for each triggered node (if Node A depends on Node B, B must be processed before A).
- Write a C++ program that reads `/app/template.conf` and generates a final configuration file at `/home/user/final_config.conf` by substituting placeholders with the Unicode values resolved from the DAG sequence.

**Stage 3: Unicode Configuration Sanitizer (Adversarial Defense)**
Configuration files often suffer from injection attacks and Unicode spoofing.
- Write a C++ command-line tool `config_sanitizer` that reads a text file and classifies it.
- The tool must correctly handle multi-language UTF-8 strings.
- It must reject (print `REJECT` to stdout and exit with code 1) any configuration containing:
  1. The Unicode Right-to-Left Override character (U+202E).
  2. Unescaped shell metacharacters (`$`, backticks, `|`, `;`) occurring outside of quotation marks.
- It must accept (print `ACCEPT` to stdout and exit with code 0) valid, safe configurations.
- Compile your tool and place the executable at `/home/user/config_sanitizer`.

Ensure all code is compiled and cleanly executable using standard coreutils and a C++ compiler (`g++`).