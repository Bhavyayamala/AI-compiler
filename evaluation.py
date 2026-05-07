import time

metrics = {
    "total_requests": 0,
    "success": 0,
    "failures": 0,
    "total_latency": 0
}

def track(start_time, errors):
    metrics["total_requests"] += 1

    latency = time.time() - start_time
    metrics["total_latency"] += latency

    if errors:
        metrics["failures"] += 1
    else:
        metrics["success"] += 1

    return {
        "latency": round(latency, 3),
        "success_rate": f"{round((metrics['success'] / metrics['total_requests']) * 100, 2)}%"
    }