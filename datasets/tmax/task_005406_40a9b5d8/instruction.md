You are a security researcher analyzing a suspicious data processing utility recovered from a compromised server. The utility, located at `/home/user/processor.py`, processes CSV files containing financial transaction data (a single column of floating-point numbers with the header `amount`). 

The incident response team has reported two strange behaviors:
1. **Statistical Anomalies & Precision Loss:** When processing certain datasets, the total sum and mean outputted by the utility slightly diverge from the true mathematical sum of the inputs. We have provided a sample dataset at `/home/user/sample_data.csv` that exhibits this precision loss. 
2. **Intermittent Failures:** The utility sometimes crashes inexplicably when processing specific, unknown input values, returning a non-zero exit code and failing to produce an output.

Your objectives are to:
1. **Analyze the Data Transformation Diff:** Compare the output of `/home/user/processor.py` against the true mathematical sum of `/home/user/sample_data.csv`. Pinpoint the exact floating-point value in the input dataset that acts as the "trigger" to activate the precision-loss mechanism (where subsequent values are maliciously truncated or altered).
2. **Fuzz Testing for Crash Reproduction:** Build a fuzzing script in a language of your choice to rapidly generate and test various floating-point inputs against `/home/user/processor.py` to discover the exact "poison" value that causes the intermittent crash (an unhandled exception/exit code 1).
3. **Report Findings:**
   - Create a file `/home/user/precision_trigger.txt` containing *only* the exact floating-point number that triggers the precision loss.
   - Create a file `/home/user/crash_trigger.txt` containing *only* the exact floating-point number that causes the program to crash.

Both files should contain a single number formatted to two decimal places (e.g., `1234.56`). You may use any tools or languages available or installable in your environment to complete this analysis.