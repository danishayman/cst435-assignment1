# Multi-Container Performance Testing Guide

## The True Benefit of Multiple Containers

The **key advantage** of multi-container setups is **parallel request handling**. When you have multiple workers, they can process requests **simultaneously**, drastically reducing total time.

## Testing Scenarios

### 1. Single Container (Baseline)
All requests are handled **sequentially** by one worker.
- Request 1 → Worker 1 (2s)
- Request 2 → Worker 1 (2s)
- Request 3 → Worker 1 (2s)
- **Total Time: 6s**

### 2. Multi-Container (Sequential Distribution)
Requests distributed across workers but still sent **one at a time**.
- Request 1 → Worker 1 (2s)
- Request 2 → Worker 2 (2s)
- Request 3 → Worker 3 (2s)
- **Total Time: 6s** (No improvement!)

### 3. Multi-Container (Parallel - THE REAL BENEFIT!)
All workers process requests **simultaneously**.
- Request 1 → Worker 1 (2s) ┐
- Request 2 → Worker 2 (2s) ├── All at the same time!
- Request 3 → Worker 3 (2s) ┘
- **Total Time: 2s** (3x speedup!)

## How to Test Multi-Container Performance

### Step 1: Start All Services

```bash
# Start single container services
docker-compose -f docker-compose-grpc-single.yml up -d
docker-compose -f docker-compose-http-single.yml up -d

# Start multi-container services (3 workers each)
docker-compose -f docker-compose-grpc-multi.yml up -d
docker-compose -f docker-compose-http-multi.yml up -d

# Verify all are running
docker ps
```

### Step 2: Run the Enhanced Benchmark

```bash
# Activate virtual environment
source venv/bin/activate

# Run comprehensive multi-container benchmark
python benchmark_multi.py --size 100 --requests 12

# Test only gRPC
python benchmark_multi.py --size 100 --requests 12 --type grpc

# Test only HTTP
python benchmark_multi.py --size 100 --requests 12 --type http
```

### Step 3: Understand the Results

The benchmark will show three different scenarios:

**Example Output:**
```
gRPC Single:                  12.0000s  (12 requests × 1.0s each)
gRPC Multi (Sequential):      12.0000s  (same as single - no benefit)
gRPC Multi (Parallel):         4.0000s  (3 workers in parallel - 3x faster!)

HTTP Single:                  15.0000s
HTTP Multi (Sequential):      15.0000s
HTTP Multi (Parallel):         5.0000s  (3x speedup!)
```

## Manual Testing (To See It Yourself)

### Test 1: Single Container (Sequential)

```bash
# Terminal 1: Start single gRPC server
docker-compose -f docker-compose-grpc-single.yml up

# Terminal 2: Send 6 requests sequentially
time python grpc_client.py --server localhost:50051 --size 100 --requests 6
# Expected: ~6 seconds (if each request takes ~1s)
```

### Test 2: Multi-Container (Parallel)

```bash
# Terminal 1: Start 3 gRPC workers
docker-compose -f docker-compose-grpc-multi.yml up

# Terminal 2-4: Send concurrent requests (open 3 terminals simultaneously)
# Terminal 2:
time python grpc_client.py --server localhost:50051 --size 100 --requests 2 &

# Terminal 3 (immediately):
time python grpc_client.py --server localhost:50052 --size 100 --requests 2 &

# Terminal 4 (immediately):
time python grpc_client.py --server localhost:50053 --size 100 --requests 2 &

# Wait for all to finish
wait

# Expected: All finish in ~2 seconds (parallel processing!)
```

## Using Python's Concurrent Requests

The `benchmark_multi.py` script demonstrates this automatically:

```python
# It uses ThreadPoolExecutor to send requests in parallel:
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    futures = [
        executor.submit(send_request, 'localhost:50051'),
        executor.submit(send_request, 'localhost:50052'),
        executor.submit(send_request, 'localhost:50053')
    ]
    # All three execute simultaneously!
```

## What You Should Observe

### Single Container Performance
- Linear scaling: 2x requests = 2x time
- One worker can only handle one request at a time
- All computation is sequential

### Multi-Container Performance (Parallel)
- Sub-linear scaling: 3x workers ≈ 3x throughput
- Multiple requests processed simultaneously
- Total wall-clock time drastically reduced

### Example with 100x100 Matrix, 12 Requests:

| Configuration | Total Time | Speedup |
|--------------|------------|---------|
| Single gRPC | 12.0s | 1.0x |
| Multi gRPC (3 workers, parallel) | 4.0s | **3.0x** |
| Single HTTP | 15.0s | 1.0x |
| Multi HTTP (3 workers, parallel) | 5.0s | **3.0x** |

## Important Notes

1. **Speedup depends on parallelism**: 
   - 3 workers can handle 3 concurrent requests
   - 12 requests ÷ 3 workers = 4 "rounds" of parallel execution

2. **Network overhead matters less in parallel**:
   - While one request waits for network, others compute
   - Better CPU utilization

3. **Real-world benefit**:
   - In production, you'd have many clients
   - Multi-container setups handle concurrent load much better

## Quick Test Script

For a quick demonstration, run:

```bash
# This will show the dramatic difference
./test_parallel.sh
```

Or manually:

```bash
# Single container test
echo "Single container test (6 requests)..."
time python grpc_client.py --server localhost:50051 --size 100 --requests 6

# Multi-container parallel test (2 requests × 3 workers)
echo "Multi-container parallel test (6 requests across 3 workers)..."
time (
  python grpc_client.py --server localhost:50051 --size 100 --requests 2 &
  python grpc_client.py --server localhost:50052 --size 100 --requests 2 &
  python grpc_client.py --server localhost:50053 --size 100 --requests 2 &
  wait
)
```

## Stopping Services

```bash
docker-compose -f docker-compose-grpc-single.yml down
docker-compose -f docker-compose-grpc-multi.yml down
docker-compose -f docker-compose-http-single.yml down
docker-compose -f docker-compose-http-multi.yml down
```

---

**Key Takeaway**: The multi-container setup shows its true value when handling **concurrent requests in parallel**, not just distributing sequential requests!
