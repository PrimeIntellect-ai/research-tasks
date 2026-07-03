You are an on-call engineer who just received a 3 AM PagerDuty alert. The critical data pipeline processing service is failing. 

The pipeline is triggered by a shell script located at `/home/user/pipeline/run_pipeline.sh`. This script pipes data from a Python ingestion service (`ingester.py`) into a Node.js processing service (`processor.js`).

According to the incident report:
1. The pipeline is currently crashing abruptly instead of processing the data.
2. The Node.js processor is throwing a stack trace that needs to be diagnosed.
3. Once the crash is resolved, it's expected that the processor will successfully output a message starting with `SUCCESS:`.
4. The upstream ingestion service relies on environment configurations to output correctly formatted data, but recent deployments might have misconfigured this.

Your tasks:
1. **Diagnose and Fix the Code:** Analyze the traceback from running `/home/user/pipeline/run_pipeline.sh`. Fix the infinite recursion/loop termination bug in `processor.js` that causes the stack overflow.
2. **Fix the Environment Misconfiguration:** Even after fixing the crash, the data parsing will fail because `ingester.py` is outputting malformed JSON. Inspect `ingester.py` to understand why it's using the wrong serialization mode, and update `/home/user/pipeline/run_pipeline.sh` to correctly configure the environment variables so that valid JSON is produced.
3. **Write a Regression Test:** Create a regression test script at `/home/user/pipeline/test_pipeline.sh`. This script must:
   - Be executable (`chmod +x`).
   - Run `/home/user/pipeline/run_pipeline.sh`.
   - Capture the output.
   - Exit with code `0` if the output contains `SUCCESS: critical`.
   - Exit with code `1` if it fails or produces any other output.

Everything you need is in the `/home/user/pipeline/` directory. You do not need root access to complete this task. Fix the pipeline so it works perfectly.