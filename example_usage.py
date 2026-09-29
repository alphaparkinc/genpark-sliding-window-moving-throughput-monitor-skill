from client import ThroughputMonitor
import time

monitor = ThroughputMonitor()
monitor.record_ttft(0.18)
start = time.time()
for i in range(20):
    monitor.record_token(start + i * 0.03) # 33 tokens/sec

stats = monitor.get_window_stats(window_seconds=2.0)
print("Throughput Statistics:", stats)
