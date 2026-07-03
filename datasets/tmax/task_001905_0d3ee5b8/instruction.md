You are an observability engineer tasked with rebuilding a legacy metric processing pipeline. The old system was driven by a compiled binary, but we need to replace it with a maintainable Bash script. 

We have a reference binary of the old system located at `/app/oracle_processor`. 
We also managed to recover a screenshot of the legacy monitoring dashboard configuration, which is saved at `/app/thresholds.png`. This image contains the critical threshold values (maximum allowed duration in milliseconds) for various service ports.

Your task is to write a Bash script at `/home/user/metric_processor.sh` that behaves EXACTLY like the reference binary.

Requirements for `/home/user/metric_processor.sh`:
1. It must read lines from standard input (stdin).
2. Each input line will contain exactly three space-separated fields: `IP PORT DURATION` (e.g., `10.0.0.5 8080 600`).
3. For each input line, the script must evaluate the duration against the threshold for that specific port (which you must extract from `/app/thresholds.png`).
4. If the port is listed in the image and the duration strictly exceeds the threshold, output: `ALERT IP PORT DURATION`
5. If the port is listed in the image and the duration is less than or equal to the threshold, output: `OK IP PORT DURATION`
6. If the port is NOT listed in the image, output: `UNKNOWN IP PORT DURATION`
7. The output must be printed to standard output (stdout), one line per input line.
8. Make sure the script is executable (`chmod +x`).

You can use `tesseract` to read the text from the image, or simply open/view it if your environment permits. The script must be written in Bash and be capable of handling an arbitrary number of input lines.