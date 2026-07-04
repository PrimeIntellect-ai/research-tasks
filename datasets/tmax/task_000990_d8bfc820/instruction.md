You are an operations engineer triaging a critical incident. Our local pricing system crashed overnight, leaving the caching database corrupted and exposing severe bugs in our C++ pricing engine. 

The system consists of two services that must run together:
1. A Python Flask API Gateway (runs on port 8000).
2. A C++ Pricing Engine daemon (runs on port 8001).
They use an SQLite database for caching pricing data.

Here is what you need to do:

1. **Database Recovery**: 
   The database at `/home/user/app/data/cache.db` is corrupted. You must recover the data. There is a backup/WAL or recovery process you can use. Save the fully recovered database to `/home/user/app/data/recovered_cache.db`. The Flask API is already configured to read from this recovered path.

2. **C++ Engine Debugging**:
   The source code for the pricing engine is in `/home/user/app/engine/engine.cpp`. It has two known issues:
   - **Infinite Loop**: The pricing calculation hangs on certain inputs. You will need to use a debugger or analyze the code to fix the loop termination condition.
   - **Precision Loss**: The results returned by the engine drift significantly from the correct values due to floating-point precision issues in the calculation loop. Fix the types and calculation to ensure high precision (at least double precision).
   Recompile the engine using `g++ -O3 -std=c++17 engine.cpp -o engine`.

3. **Service Composition**:
   Once the database is recovered and the engine is fixed and recompiled, you must bring up the services:
   - Start the C++ engine: `/home/user/app/engine/engine` (listens on port 8001).
   - Start the Flask gateway: `python3 /home/user/app/gateway/app.py` (listens on port 8000).

4. **Verification**:
   The system must correctly serve end-to-end pricing requests. You can test the system by querying `http://localhost:8000/price?id=...`.
   We have a test suite that will calculate the Mean Squared Error (MSE) of your API's responses against a high-precision reference. 
   Leave the services running in the background. The automated verifier will test your setup and measure the MSE. Your goal is to achieve an MSE of less than `1e-8`.