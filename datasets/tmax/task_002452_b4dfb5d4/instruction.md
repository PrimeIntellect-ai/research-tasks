You are a platform engineer maintaining a CI/CD pipeline for a high-performance numerical computing platform. Users submit C++ snippets containing optimized numerical algorithms (and occasionally inline assembly), which are built and executed by the platform.

The system is currently failing on multiple fronts, and you need to restore the pipeline and secure it against malicious payloads.

The system components are located in `/home/user/app/`:
1. **API Gateway**: An Nginx server configured in `/home/user/app/nginx/nginx.conf`.
2. **Submission API**: A Flask application in `/home/user/app/api/app.py`.
3. **Queue**: A Redis instance.
4. **Build Worker**: A C++ daemon in `/home/user/app/worker/`.

Your objectives:

**1. Service Reconfiguration (Multi-service Integration)**
The services are currently misconfigured and cannot communicate. You must fix the configuration files so that:
- Nginx listens on port `8080` and proxies requests for `/api/submit` to the Flask API.
- The Flask API runs on port `5000` and successfully connects to Redis.
- The C++ build worker connects to the same Redis instance to pop submissions.
*Note: A startup script `/home/user/app/start_services.sh` is provided to launch all services. You must modify the config files/environment variables so the end-to-end flow works.*

**2. Makefile Repair**
The `Makefile` in `/home/user/app/worker/` is broken. It fails to correctly link the object files for the build worker daemon, particularly failing to link the `hiredis` and `pthread` libraries. Fix the `Makefile` so that running `make` successfully produces the `worker_daemon` executable.

**3. Adversarial Payload Sanitizer**
Users are submitting malicious C++ code (e.g., inline assembly containing `syscall` or system command execution) disguised as numerical algorithms. 
You must implement a C++ static analyzer in `/home/user/app/sanitizer.cpp` and compile it to `/home/user/app/sanitizer`.

The sanitizer must:
- Accept a single command-line argument: the path to a C++ source file.
- Read and analyze the source file.
- Exit with code `0` (Clean) if the file contains a legitimate numerical algorithm.
- Exit with code `1` (Evil) if the file contains malicious system calls, `#include <unistd.h>`, `#include <stdlib.h>`, `system(`, or inline assembly `__asm__` attempting raw `syscall`s or interrupts (e.g., `int 0x80`).

We have provided test corpora in `/home/user/app/corpora/`:
- `/home/user/app/corpora/clean/`: Contains valid numerical implementations (e.g., matrix multiplication, FFT).
- `/home/user/app/corpora/evil/`: Contains malicious submissions attempting to execute shellcode or unauthorized binaries.
Your sanitizer will be tested against these exact files.

Once you have completed all tasks, leave the compiled `sanitizer` binary in `/home/user/app/` and ensure the `worker_daemon` compiles successfully. Do not leave the services running; the verification script will start them as needed.