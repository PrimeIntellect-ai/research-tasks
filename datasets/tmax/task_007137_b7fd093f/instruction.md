You are an operations engineer triaging a severe incident. Our custom environmental monitoring service crashed overnight, corrupting its main database. Fortunately, it writes incoming data to a Write-Ahead Log (WAL) before committing, so we should be able to recover the lost records.

There are three parts to this incident recovery:

**1. Log Timeline Reconstruction**
The monitoring system consists of two microservices that log to `/home/user/logs/collector.log` and `/home/user/logs/processor.log`. They use different timestamp formats and occasionally report out of order.
Find the exact timestamp of the final "FATAL_CRASH" event that brought the system down. Write ONLY this exact timestamp (exactly as it appears in the log, whether ISO8601 or epoch) to `/home/user/crash_time.txt`.

**2. Tool Compilation & Debugging**
The previous engineer wrote a C-based recovery tool located in `/home/user/src/`. However, it currently fails to compile due to linker errors. 
Furthermore, QA reported that before the crash, the tool was outputting incorrect temperature values. The system records data in Celsius, but the recovery tool is supposed to convert this to Fahrenheit before writing the CSV. Check the conversion formula in the source code and correct it.

**3. Database Recovery**
Once you have fixed and successfully compiled the recovery tool (using the provided `Makefile`), run it against the corrupted WAL file located at `/home/user/data/sensor.wal`. 
The tool expects the input WAL file as the first argument and the output CSV file as the second argument.
Save the recovered records to `/home/user/recovered_data.csv`.

Ensure all requested output files (`/home/user/crash_time.txt` and `/home/user/recovered_data.csv`) are created with the exact names and paths specified.