I need you to debug a long-running Python image processing service that is suffering from a severe memory leak, intermittent failures, and a subtle precision loss issue under concurrent load. 

The service is located at `/home/user/image_service.py`. It exposes a multithreaded HTTP endpoint on port 8080 that receives requests to process images and calculate a specialized mathematical signature (using singular value decomposition and gradient calculations). We have a test image located at `/app/reference_sample.png`.

Currently, when the service runs under concurrent load, two things happen:
1. The memory usage grows unbounded until the service is killed by the OOM killer.
2. The calculated signature for `/app/reference_sample.png` intermittently loses precision, returning a corrupted floating-point array due to what we suspect is a race condition in the shared math cache.

Your task is to:
1. Identify and fix the memory leak in `/home/user/image_service.py`.
2. Diagnose the traceback logs we captured during intermittent failures, and fix the race condition causing the precision loss in the concurrent math operations.
3. Ensure the service can process 500 concurrent requests without exceeding 150MB of RSS memory.

To complete the task, modify `/home/user/image_service.py` to resolve these issues. Leave the modified file in its original location. We will test your fixed service by running a load test and measuring both the peak memory consumption and the Mean Squared Error (MSE) of the image signatures against our golden reference.