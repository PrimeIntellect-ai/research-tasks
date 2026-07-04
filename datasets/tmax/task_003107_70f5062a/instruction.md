You are acting as a capacity planner for our infrastructure. We are migrating our old resource monitoring systems and need to recreate our process-filtering logic.

Unfortunately, our original capacity planning threshold rules were lost, but we have a screenshot of the old dashboard's configuration panel saved at `/app/capacity_rules.png`.

Your task is to:
1. Extract the resource limit rules and the "Ignore Path" regular expression from the image `/app/capacity_rules.png`. (You can use `tesseract` or any other tool to read the image).
2. Write a classification script at `/home/user/classify_hog.py` (or any language of your choice, ensure it has the correct shebang and is executable).
3. The script must read a single line of comma-separated text from standard input representing process metrics in the format: `PID,USER,CPU_PERCENT,MEM_PERCENT,COMMAND`.
4. The script must evaluate the input against the rules extracted from the image:
   - If the process exceeds *either* the CPU threshold OR the Memory threshold, AND the `COMMAND` does *not* match the "Ignore Path" regular expression, the script must print exactly `REJECT` to standard output.
   - Otherwise, the script must print exactly `ACCEPT` to standard output.
5. The script must act purely as a text-processing and decision pipeline for the single input line. 

Ensure your script is robust and correctly handles floats for the percentages. Do not include any other output (like debug logs) on standard output, as it will be evaluated programmatically.