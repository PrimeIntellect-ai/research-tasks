You are an Site Reliability Engineer investigating a critical false-alert issue in our custom uptime monitoring service. 

Our containerized monitoring service, written in C++, processes millions of ping events to calculate our monthly uptime SLA. Recently, it has been triggering false alerts, claiming our uptime is dropping below our strict target SLA, even though there are no actual outages. 

We suspect there are two issues:
1. **Build/Dependency Issue**: The service is currently failing to build inside its container environment due to a dependency conflict between the logging library (`libfmt`) and our custom monitoring framework. You will need to inspect the container build logs or build it locally to resolve this dependency conflict in the `CMakeLists.txt`.
2. **Floating-point Precision Issue**: Once built, the service accumulates uptime over millions of small time increments. We suspect it is suffering from catastrophic cancellation or precision loss, causing the calculated uptime to fall artificially. 

There is a dashboard screenshot saved at `/app/alert_dashboard.png` which shows the Target SLA percentage we are supposed to meet. You will need to extract this target SLA to understand the expected precision.

Your tasks:
1. Navigate to `/home/user/uptime_monitor`.
2. Fix the dependency conflict in the `CMakeLists.txt` so the project compiles successfully using `cmake` and `make`.
3. Debug and repair the floating-point precision issue in `src/uptime_calculator.cpp`. The calculator must accurately sum millions of milliseconds of uptime without losing precision. (Hint: consider using a more robust summation algorithm or appropriate data types).
4. Run the compiled executable `./uptime_monitor data/ping_logs.csv` and redirect its final percentage output (just the number, e.g., `99.999123`) to `/home/user/calculated_sla.txt`.

Ensure your final output in `/home/user/calculated_sla.txt` is highly accurate.