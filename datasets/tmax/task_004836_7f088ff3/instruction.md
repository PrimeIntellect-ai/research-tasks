You are an operations engineer triaging a critical incident in our data pipeline. Our proprietary legacy data processor, a C++ executable, has been crashing continuously in production with segmentation faults. We only have the stripped binary available at `/app/processor_bin`.

I have collected network packet captures from the time of the crashes in `/home/user/pcaps/` and the container application logs in `/home/user/crash.log`. We suspect that a specific boundary condition or off-by-one error in certain incoming payloads is triggering the crash.

Your task is to:
1. Analyze the pcaps and logs to extract the payloads that cause the crash.
2. Use the stripped binary `/app/processor_bin` to reproduce the crashes and deduce the exact structure and boundary condition of the "poison" payloads.
3. Write a C++ classifier, `/home/user/detector.cpp`, and compile it to `/home/user/detector`.
4. The detector must take exactly one argument (the file path to a binary payload) like so: `/home/user/detector <payload_file>`
5. It must exit with code `0` if the payload is safe (clean), and exit with code `1` if the payload exhibits the crash-inducing malformed property (evil).

You must ensure your detector is highly accurate and does not flag legitimate, safe edge cases as evil, while catching 100% of the crash-inducing payloads. Do not rely on hardcoded hashes; you must parse and check the structural condition causing the issue.