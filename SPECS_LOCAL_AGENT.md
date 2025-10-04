
This file contains the detailed technical specifications for the local Python server.

# SPECIFICATION: Local Agent Server (Python)

## 1\. Framework & Orchestration

  - The server will be a **Flask** web application.[14, 15, 16]
  - The entire application will be orchestrated and run by **OpenHands**.[17, 18, 19]

## 2\. Project Setup (`requirements.txt`)

flask
flask-cors
openai
structifyai
ddtrace
datadog
python-json-logger

````

## 3. Server Logic (`app.py`)

### 3.1. Flask Server & CORS
- Instantiate a standard Flask app.
- **Crucially, configure CORS** using `flask-cors` to only allow requests from the Chrome extension's origin (`chrome-extension://<ID>`). A wildcard `*` is acceptable for the hackathon but specifying the origin is best practice.[20, 21, 22, 23]
- Create a single API endpoint: `@app.route('/data', methods=)`.

### 3.2. AI & Data Processing
- The `/data` endpoint will receive a JSON payload containing the subtitle text.
- **Structify:** Use the Structify Python SDK to process the raw text. Initialize the client and use it to structure the incoming data.[24, 25, 26, 27, 28, 29]
- **TrueFoundry AI Gateway:** All calls to OpenAI will be routed through the TrueFoundry Gateway.
  - The OpenAI client will be initialized with a `base_url` and `api_key` provided by TrueFoundry and set as environment variables.[30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42]
  - **CODE EXAMPLE:**
    ```python
    from openai import OpenAI
    import os

    client = OpenAI(
        api_key=os.environ.get("TRUEFOUNDRY_API_KEY"),
        base_url=os.environ.get("TRUEFOUNDRY_BASE_URL")
    )
    ```
- **OpenAI:** Use the configured `client` to call the Chat Completions API. The prompt should ask the model to determine if the text describes a loud noise and respond with a simple "YES" or "NO".[43, 44, 45, 46, 47, 48]

### 3.3. Datadog Observability
- **APM (Auto-Instrumentation):** The application will be launched using `ddtrace-run`. This requires no code changes. The `Dockerfile` or `docker-compose.yml` `CMD` should be `["ddtrace-run", "python", "app.py"]`.[49, 50, 51, 52, 53, 54, 55, 56]
- **Structured Logging:**
  - Configure logging to output in JSON format using a library like `python-json-logger`.[57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68]
  - **Crucially, enable log injection** by setting the environment variable `DD_LOGS_INJECTION=true`. This automatically adds `dd.trace_id` and `dd.span_id` to logs for correlation.[64]
- **Custom Metrics (DogStatsD):**
  - Initialize the `statsd` client from the `datadog` library.
  - **CODE EXAMPLE:**
    ```python
    from datadog import statsd

    # When a loud event is detected
    statsd.increment('crest.loud_event.detected', tags=["video_id:<id>"])

    # When a volume adjustment is successful
    statsd.gauge('crest.volume.adjustment.level', 0.5, tags=["video_id:<id>"])
    ```

## 4. Environment Variables (`.env`)
The agent will need to be configured with the following environment variables.
````

# TrueFoundry

TRUEFOUNDRY\_API\_KEY="tfy-..."
TRUEFOUNDRY\_BASE\_URL="https://..."

# OpenAI (via TrueFoundry)

OPENAI\_API\_KEY="tfy-..." \# Same as above

# Datadog

DD\_AGENT\_HOST="localhost"
DD\_LOGS\_INJECTION="true"
DD\_SERVICE="crest-agent"
DD\_ENV="development"
DD\_VERSION="0.1.0"

```
```