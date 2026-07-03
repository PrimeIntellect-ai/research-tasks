We have a long-running image processing service written in Python that relies on a custom C extension for performance. Recently, the service has been suffering from two major issues:
1. **Memory Leak**: The service's memory usage grows unbounded when processing requests, eventually leading to OOM kills.
2. **Numerical Instability / Overflow**: Under certain configurations, the C extension computes completely wrong results due to an integer overflow during pixel accumulation.

A recent bug report was screenshotted and saved at `/app/bug_report.png`. It contains the exact "intensity multiplier" parameter that triggers the severe numerical overflow in our production environment. 

Your task is to:
1. Analyze `/app/bug_report.png` (you may use `tesseract` to read the text) to extract the problematic intensity multiplier.
2. Investigate the Python service located at `/home/user/img_service/`. The service uses a C extension (`processor.c`) built via `setup.py`.
3. Create a minimal reproducible example or fuzzer script to pinpoint the memory leak and the overflow.
4. Fix the memory leak in `processor.c`.
5. Fix the integer overflow in `processor.c` so that it computes the correct moving average and accumulation without wrapping around, even for bright images and high multipliers. 
6. Rebuild the C extension and start the service in the background on port `8000`. The service must be running via `python server.py`.
7. Write the extracted intensity multiplier to `/home/user/img_service/multiplier.txt` as a single float.

The automated verification system will run a high-volume load test against your running server on port 8000. It will measure the memory growth (in MB) over 10,000 requests and check the numerical correctness of the outputs.

Ensure the fixed service is running on port `8000` when you finish!