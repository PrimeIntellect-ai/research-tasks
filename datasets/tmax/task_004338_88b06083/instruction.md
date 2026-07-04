You are tasked with setting up a polyglot build system from scratch, translating a legacy text sanitizer, and integrating it into a multi-service backend.

We have a broken Python setup for an API gateway that previously relied on a legacy C extension to sanitize text inputs. The C code is lost, but the logic requirement is known. You must write a new Rust-based shared library, manage its ABI, integrate it into a Python package via `ctypes`, and configure a multi-service architecture (Flask + Redis) to use it.

**Stage 1: Code Translation & ABI Management**
Create a new Rust project in `/home/user/sanitizer_project`.
Implement a Rust library that compiles to a shared object (`.so`). It must expose a C-compatible ABI function:
`bool is_clean(const char* input_string);`
The function must return `false` if the input string contains ANY of the following malicious patterns (case-insensitive):
- `<script>`
- `javascript:`
- `union select`
Otherwise, it must return `true`.
Ensure you handle memory safety safely across the FFI boundary. 

**Stage 2: Adversarial Corpus Verification**
Your Rust function must perfectly classify two corpora provided in `/home/user/data/`:
- `/home/user/data/evil/`: Contains 50 malicious payloads. Your function MUST reject 100% of these (return `false`).
- `/home/user/data/clean/`: Contains 50 benign texts. Your function MUST preserve/accept 100% of these (return `true`).
You can write your own Python script using `ctypes` to load your shared library and test against these files. 

**Stage 3: Polyglot Build System Setup**
The python package in `/home/user/app/` has a broken `pyproject.toml`.
Instead of fighting the broken C-extension build, write a shell script `/home/user/app/build.sh` that:
1. Compiles your Rust project in release mode.
2. Copies the compiled `.so` file to `/home/user/app/libsans.so`.
Provide a Python file `/home/user/app/wrapper.py` that uses `ctypes` to load `libsans.so` and exposes a Python function `def check_text(text: str) -> bool:`.

**Stage 4: Multi-Service Configuration**
The application uses Flask (API) and Redis (Cache/Rate Limiting).
In `/home/user/app/`, there is a `start.sh` script that brings up Redis on port 6379 and Flask on port 5000.
1. Modify `/home/user/app/config.env` to set `REDIS_URL=redis://localhost:6379` and `SAN_LIB_PATH=/home/user/app/libsans.so`.
2. The Flask app expects `wrapper.py` to be importable and functioning. 
3. Run `./start.sh`.

When complete, an automated verifier will send HTTP POST requests to `http://localhost:5000/submit` with JSON `{"text": "<payload>"}`. The end-to-end flow must return `200 OK` for clean payloads and `403 Forbidden` for evil payloads.
Leave the services running in the background when you are done.