You are acting as a cloud architect migrating a set of legacy microservices to a new environment. 

We have a custom, lightweight Python-based process supervisor located at `/home/user/supervisor.py`. It reads a configuration file at `/home/user/services.json` and launches the services. 

However, the current implementation of `supervisor.py` is too simplistic. It starts all services simultaneously and ignores environment variable requirements, causing the dependent migration worker to crash on startup because the data service isn't ready yet (a classic missing `After=` dependency issue, similar to systemd).

Your task is to fix `/home/user/supervisor.py` so that it handles the service lifecycle correctly. You must implement the following logic in `supervisor.py`:
1. **Dependency Ordering:** Parse the `depends_on` key in `services.json`. A service must not be started until the service it depends on has been started.
2. **Readiness Checking:** It's not enough to just start the dependency; you must wait until it is actually ready. If a service definition includes a `port` key, your supervisor must actively poll `127.0.0.1` on that port and wait until it accepts TCP connections before launching any dependent services.
3. **Environment Variable Setup:** If a service definition contains an `env` dictionary, those environment variables must be injected into the process's environment when it is spawned (without removing the system's existing environment variables).

Once you have fixed `supervisor.py`, run it (e.g., `python3 /home/user/supervisor.py`). 

The `migration_worker` service will attempt to connect to the `data_service`. If the environment variables are correct and the dependency is fully ready, the worker will succeed and automatically write a final success state to `/home/user/status.log`. 

The task is complete when `/home/user/status.log` exists and contains the successful migration message. Do not modify `services.json`, `data_service.py`, or `worker.py`. Focus exclusively on fixing `supervisor.py` and running it.