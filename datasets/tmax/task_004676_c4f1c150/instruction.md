You have inherited an unfamiliar IoT data ingestion system located in `/app/iot_system`. The system comprises multiple services that parse binary sensor data and store it. 

There are currently two major issues:
1. The `parser_service.py` is failing to authenticate with the `ingest_api.py` service. The API token was lost. However, a developer previously accidentally committed a network packet capture (`capture.pcap`) containing valid traffic between the parser and the ingest API, before deleting it in a subsequent commit.
2. The system works fine for most sensor readings, but occasionally produces absurdly high temperature values when the environment gets cold, causing downstream analytics to fail. The binary payload from sensors is exactly 16 bytes: a 4-byte magic string (`IOT\x00`), a 32-bit unsigned integer for the sensor ID, a 32-bit unsigned integer for the timestamp, and a 32-bit integer for the temperature (in milli-Celsius). All integers are little-endian.

Your task:
1. Use Git history forensics to recover the deleted `capture.pcap` file.
2. Analyze the pcap file to extract the valid HTTP Bearer authentication token used to communicate with the `ingest_api.py`.
3. Update `parser_service.py` with the correct token.
4. Debug and fix the format parsing logic in `parser_service.py` so that negative temperatures are correctly processed (beware of integer overflows/underflows caused by incorrect data types).
5. Start the services using the provided `/app/iot_system/startup.sh` script.

The automated verifier will act as an external sensor and an admin client. It will:
- Send custom binary UDP packets to the `parser_service` at `127.0.0.1:5005`.
- Query the `parser_service`'s admin interface at `http://127.0.0.1:8081/latest?sensor_id=<id>` to verify that the data was correctly parsed, accepted by the ingest API, and stored.

Leave the services running in the background when you are done. Do not change the ports that the services are configured to use.