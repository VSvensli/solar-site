from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST, Summary, Gauge
from fastapi.responses import Response
from fastapi import APIRouter

router = APIRouter(prefix="")

import time
import random

# Create some metrics
REQUEST_TIME = Summary("request_processing_seconds", "Time spent processing request")
REQUEST_COUNT = Counter("http_requests_total", "Total number of HTTP requests")
IN_PROGRESS = Gauge("inprogress_requests", "Number of requests in progress")
LATENCY_HISTOGRAM = Histogram("request_latency_seconds", "Request latency")


@router.get("/test_metrics")
def test_metrics():
    process_request()
    return {"message": "This is a test endpoint."}


@REQUEST_TIME.time()
def process_request():
    IN_PROGRESS.inc()
    REQUEST_COUNT.inc()
    latency = random.random()
    LATENCY_HISTOGRAM.observe(latency)
    time.sleep(latency)
    IN_PROGRESS.dec()


@router.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
