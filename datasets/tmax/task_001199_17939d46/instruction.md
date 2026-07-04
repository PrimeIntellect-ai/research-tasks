You need to fix and complete our capacity planning pipeline. The pipeline consists of a data aggregator, a log sender, and a capacity planning analyzer. 

Here are your tasks:

1. **System Config Management & Service Startup:**
   The data aggregator script is located at `/home/user/pipeline/aggregator.py`. It reads its settings from `/home/user/pipeline/config.ini`.
   - Edit the configuration file so that the aggregator binds to port `8080` (it is currently misconfigured).
   - The `aggregator.py` script requires interactive authentication upon startup. It will prompt `Enter PIN: `.
   - Write an expect script at `/home/user/pipeline/start_agg.exp` that launches `python3 /home/user/pipeline/aggregator.py`, waits for the `Enter PIN: ` prompt, sends the PIN `7788`, and then hands over control (using `interact` or keeping the process alive so it continues running in the background).

2. **Process Monitoring & Control:**
   Once you have the expect script working, start the aggregator in the background. Ensure it is actively listening on port 8080. (You do not need to generate any logs yourself; our integration test will verify the service flow by sending data to port 8080 and checking the aggregator's output).

3. **Capacity Planner Implementation:**
   We need a standalone Python script that acts as the capacity planner analyzer, located at `/home/user/planner.py`.
   - The script must read text lines continuously from standard input (`sys.stdin`) until EOF.
   - It should strictly look for lines matching the exact format:
     `DATA node=<hostname> cpu=<int> mem=<int> disk=<int>`
     (where `<hostname>` is an alphanumeric string, and the others are integers. There is exactly one space between each field).
   - For every valid line, calculate a capacity score using integer arithmetic:
     `SCORE = (cpu * 2) + (mem // 10) + (disk * 5)`
   - If `SCORE > 500`, print to standard output: `ALERT <hostname> <SCORE>`
   - If `SCORE <= 500`, print to standard output: `OK <hostname> <SCORE>`
   - Any line that does not strictly match the format (or contains non-integer values for cpu/mem/disk) must be completely ignored (print nothing for that line).

Your `planner.py` will be tested exhaustively against a hidden oracle implementation with thousands of fuzzed inputs. It must match the expected output exactly, byte-for-byte.