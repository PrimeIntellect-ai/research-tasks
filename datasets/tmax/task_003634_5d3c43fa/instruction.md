You are an operations engineer triaging a critical incident for an internal ticket-booking system. The system recently crashed and is now deadlocking under high contention. Furthermore, the crash corrupted our primary database, and we lost the payment gateway API key that was injected via environment variables.

You have been granted access to the application directory at `/app/`. Here is the current state of the system:
- `/app/services/`: Contains the source code for the microservices.
  - `api_gateway.py`: The frontend API service.
  - `ticket_worker.py`: A multithreaded background worker that processes orders. It currently deadlocks under high load and has a connection pool exhaustion issue.
  - `payment_mock.py`: A mock payment gateway that requires authentication.
- `/app/data/`: Contains `bookings.db` (which appears corrupted) and `bookings.db-wal` (the Write-Ahead Log containing uncommitted transactions right before the crash).
- `/app/dumps/`: Contains `worker_crash.core`, a memory dump of the `ticket_worker` process taken right after it crashed.
- `/app/start_services.sh`: A script to launch all three services.

Your objectives:
1. **API Key Recovery**: The `payment_mock.py` requires a `PAYMENT_API_KEY` environment variable. The key was in memory when the process crashed. Extract the API key (format: `PAYMENT_SEC_[A-Za-z0-9]+`) from the `/app/dumps/worker_crash.core` memory dump, and configure the services to use it (e.g., by creating an `/app/.env` file that `start_services.sh` can read, or exporting it).
2. **Database Recovery**: Recover the SQLite database `/app/data/bookings.db` using the WAL file so that the uncommitted records are fully restored and the database is accessible again without corruption errors.
3. **Debug the Worker**: Fix `ticket_worker.py`. 
   - Identify and fix the deadlock condition occurring when threads try to acquire multiple resources.
   - Fix an off-by-one boundary condition in the custom resource pool that causes connection exhaustion under high contention.
4. **Integration & Tuning**: Ensure all services can start correctly using `./start_services.sh`. 

Once the services are running and fixed, run the load test script located at `/app/tests/load_test.py`. It will send concurrent requests to the API gateway. The system must process transactions without deadlocking. 

Save the output of your load test to `/home/user/load_test_results.txt`. To succeed, your fixed system must achieve a throughput of at least 800 successful bookings per second.