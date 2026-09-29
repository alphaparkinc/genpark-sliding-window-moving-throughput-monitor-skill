# genpark-sliding-window-moving-throughput-monitor-skill

Sliding window performance monitor computing generation velocity (TPS), Time-To-First-Token (TTFT), and Inter-Token Latency (ITL) distributions.

## Architecture

```mermaid
flowchart LR
    TokenEvents[Token Arrival Timestamps] --> Monitor[ThroughputMonitor]
    Monitor --> SlidingWindow[Sliding Window Filter]
    SlidingWindow --> TPS[TPS Calculation]
    SlidingWindow --> ITL[ITL P50/P90 Quantiles]
    SlidingWindow --> TTFT[TTFT Latency Capture]
```

## Features
- **High-Resolution Telemetry**: Sub-millisecond latency distribution calculations.
- **Percentile Distributions**: Evaluates P50 and P90 tail latencies.
- **Standard Library Only**: 100% Python stdlib.
