"""Sliding Window Moving Throughput Monitor.
100% Python Standard Library.
"""

import time

class ThroughputMonitor:
    """Measures real-time LLM token generation velocity, TTFT, and inter-token latencies."""
    def __init__(self):
        self.timestamps = []
        self.ttft_seconds = None

    def record_ttft(self, ttft: float):
        self.ttft_seconds = ttft

    def record_token(self, timestamp: float = None):
        if timestamp is None:
            timestamp = time.time()
        self.timestamps.append(timestamp)

    def get_window_stats(self, window_seconds: float = 10.0, current_time: float = None) -> dict:
        if not self.timestamps:
            return {"total_tokens": 0, "tps": 0.0, "mean_itl_ms": 0.0}

        if current_time is None:
            current_time = self.timestamps[-1]

        cutoff = current_time - window_seconds
        window_stamps = [t for t in self.timestamps if t >= cutoff]

        total_tokens = len(self.timestamps)
        window_tokens = len(window_stamps)

        if window_tokens >= 2:
            duration = window_stamps[-1] - window_stamps[0]
            tps = (window_tokens - 1) / max(duration, 1e-4)
            itls = [(window_stamps[i] - window_stamps[i-1]) * 1000 for i in range(1, len(window_stamps))]
            itls_sorted = sorted(itls)
            mean_itl = sum(itls) / len(itls)
            p50 = itls_sorted[len(itls_sorted) // 2]
            p90 = itls_sorted[int(len(itls_sorted) * 0.9)]
        else:
            tps = 0.0
            mean_itl = 0.0
            p50 = 0.0
            p90 = 0.0

        return {
            "total_tokens": total_tokens,
            "window_tokens": window_tokens,
            "tps": round(tps, 2),
            "mean_itl_ms": round(mean_itl, 2),
            "p50_itl_ms": round(p50, 2),
            "p90_itl_ms": round(p90, 2),
            "ttft_seconds": round(self.ttft_seconds, 4) if self.ttft_seconds else None
        }
