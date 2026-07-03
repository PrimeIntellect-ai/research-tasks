You are a capacity planner tasked with analyzing resource usage for an upcoming peak traffic event. Our monitoring system exports raw usage logs in UTC, but our planning committee needs the projections localized to `Europe/Berlin` and scaled by our expected growth multiplier.

Your task is to create a Python script at `/home/user/projector.py` that processes these logs and generates the projected capacity.

Requirements:
1. We have a snapshot of the latest capacity planning dashboard saved at `/app/dashboard_snapshot.png`. You need to extract the "Peak Multiplier" from this image (it will be a decimal number).
2. Your script `/home/user/projector.py` must read CSV lines from standard input (`sys.stdin`).
3. The input format is: `timestamp_utc,service_name,cpu_cores,memory_mb`
   Example: `2023-11-01T14:30:00Z,checkout-service,2.5,4096.0`
4. For each line, the script must:
   - Convert the UTC timestamp to the `Europe/Berlin` timezone.
   - Format the new timestamp as `YYYY/MM/DD HH:MM:SS`.
   - Multiply the `cpu_cores` and `memory_mb` by the Peak Multiplier you found in the image.
   - Round both projected values to exactly 2 decimal places.
5. Output the result to standard output in the following format:
   `[Local_Timestamp] service_name: CPU=Projected_CPU, MEM=Projected_Mem`
   Example: `[2023/11/01 15:30:00] checkout-service: CPU=3.62, MEM=5939.20`
   
Ensure your script can handle arbitrary lengths of standard input and processes them line by line. Do not print any extra debugging information to stdout. Ensure the script is executable.

Note: You can use `tesseract` to read the image if necessary.