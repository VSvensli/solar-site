from prometheus_client import start_http_server, Summary, Counter, Gauge, Histogram
import time
import random

# Create some metrics
REQUEST_TIME = Summary("request_processing_seconds", "Time spent processing request")
REQUEST_COUNT = Counter("http_requests_total", "Total number of HTTP requests")
IN_PROGRESS = Gauge("inprogress_requests", "Number of requests in progress")
LATENCY_HISTOGRAM = Histogram("request_latency_seconds", "Request latency")


@REQUEST_TIME.time()
def process_request():
    IN_PROGRESS.inc()
    REQUEST_COUNT.inc()
    latency = random.random()
    LATENCY_HISTOGRAM.observe(latency)
    time.sleep(latency)
    IN_PROGRESS.dec()


if __name__ == "__main__":
    start_http_server(8001)  # Prometheus scrapes this endpoint
    while True:
        time.sleep(2)
        process_request()
