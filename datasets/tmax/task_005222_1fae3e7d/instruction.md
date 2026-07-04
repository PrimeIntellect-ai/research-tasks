You are a localization engineer tasked with building a translation update service. We have a video file located at `/app/presentation.mp4` containing a technical presentation. We are generating localized subtitles for this video.

Your task is to write a Go service that provides a translation validation and processing API. The service must run as an HTTP server and do the following:

1. **Video Analysis**: Use `ffmpeg` (which is pre-installed) to extract frame metadata from `/app/presentation.mp4`. We are specifically interested in detecting black frames or silent periods (you can choose an appropriate threshold) to identify logical scene boundaries where subtitles should not overlap.
2. **Translation Processing API**: Implement an HTTP POST endpoint at `/api/v1/translations/process`. It will receive JSON payloads containing an array of subtitle segments: `{"startTime": float, "endTime": float, "text": string, "confidence": float}`.
3. **Imputation & Interpolation**: Sometimes our STT (Speech-to-Text) engine misses segments. If there is a gap between two segments greater than 2.0 seconds but less than 5.0 seconds, your service must interpolate a placeholder segment (e.g., `[MISSING AUDIO]`) spanning the gap. 
4. **Rolling Statistics**: Calculate a rolling average of the `confidence` score over a window of 3 adjacent segments. Include this rolling average in the response payload for each segment.
5. **Constraint-based Validation**: Validate that no subtitle segment overlaps with the scene boundaries (black/silent frames) detected in step 1. If an overlap occurs, adjust the `endTime` of the preceding segment or the `startTime` of the following segment to respect the boundary. No segment should exceed 7 seconds in duration.
6. **Server Details**: The Go server must listen on `127.0.0.1:8080`. It must accept an `Authorization` header with the bearer token `LOCALIZATION_ENGINEER_TOKEN_99`.

The response from the `/api/v1/translations/process` endpoint should be a JSON array of the processed and validated segments, including the interpolated placeholders, adjusted timestamps, and the `rollingConfidence` field.

Ensure your Go code is well-structured and handles edge cases (e.g., empty payloads). Start the server in the background so it can be tested.