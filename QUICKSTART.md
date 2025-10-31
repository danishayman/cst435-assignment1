# Matrix Multiplication Service - Quick Start Guide

## What's Been Created

I've implemented a complete Matrix Multiplication Service with 4 different configurations to compare performance:

1. **Single container gRPC** - Client & server on same machine
2. **Multi-container gRPC** - Client + 3 worker containers
3. **Single container HTTP** - Same using Flask
4. **Multi-container HTTP** - 3 Flask workers

## Files Created

### Core Implementation
- `matrix.proto` - Protocol Buffer definition for gRPC
- `grpc_server.py` - gRPC server implementation
- `grpc_client.py` - gRPC client implementation
- `http_server.py` - Flask/HTTP server implementation
- `http_client.py` - HTTP client implementation

### Docker Configuration
- `Dockerfile.grpc` - Docker image for gRPC server
- `Dockerfile.http` - Docker image for HTTP server
- `docker-compose-grpc-single.yml` - Single gRPC container
- `docker-compose-grpc-multi.yml` - 3 gRPC worker containers
- `docker-compose-http-single.yml` - Single HTTP container
- `docker-compose-http-multi.yml` - 3 HTTP worker containers

### Utilities
- `benchmark.py` - Performance comparison script
- `setup.sh` - Setup script
- `requirements.txt` - Python dependencies
- `README.md` - Full documentation

## Quick Start

### Option 1: Run Locally (Simplest)

#### Test gRPC:
```bash
# Terminal 1 - Start server
python3 grpc_server.py

# Terminal 2 - Run client
python3 grpc_client.py --size 50 --requests 10
```

#### Test HTTP:
```bash
# Terminal 1 - Start server
python3 http_server.py

# Terminal 2 - Run client
python3 http_client.py --size 50 --requests 10
```

### Option 2: Run with Docker

#### Single Container gRPC:
```bash
# Start server
docker-compose -f docker-compose-grpc-single.yml up --build

# In another terminal, test it
python3 grpc_client.py --server localhost:50051 --size 50 --requests 10
```

#### Multi-Container gRPC (3 workers):
```bash
# Start all 3 workers
docker-compose -f docker-compose-grpc-multi.yml up --build

# Test each worker
python3 grpc_client.py --server localhost:50051 --size 50 --requests 10
python3 grpc_client.py --server localhost:50052 --size 50 --requests 10
python3 grpc_client.py --server localhost:50053 --size 50 --requests 10
```

#### Single Container HTTP:
```bash
# Start server
docker-compose -f docker-compose-http-single.yml up --build

# Test it
python3 http_client.py --server http://localhost:5000 --size 50 --requests 10
```

#### Multi-Container HTTP (3 workers):
```bash
# Start all 3 workers
docker-compose -f docker-compose-http-multi.yml up --build

# Test each worker
python3 http_client.py --server http://localhost:5001 --size 50 --requests 10
python3 http_client.py --server http://localhost:5002 --size 50 --requests 10
python3 http_client.py --server http://localhost:5003 --size 50 --requests 10
```

## Performance Comparison

To run a complete benchmark comparing all configurations:

```bash
# Start all services (in separate terminals or with -d flag)
docker-compose -f docker-compose-grpc-single.yml up -d
docker-compose -f docker-compose-grpc-multi.yml up -d
docker-compose -f docker-compose-http-single.yml up -d
docker-compose -f docker-compose-http-multi.yml up -d

# Run benchmark
python3 benchmark.py --size 50 --requests 20
```

## Client Options

Both clients support these arguments:

### gRPC Client:
```bash
python3 grpc_client.py --server localhost:50051 --size 50 --requests 10
```
- `--server`: Server address (default: localhost:50051)
- `--size`: Matrix size NxN (default: 50)
- `--requests`: Number of requests (default: 10)

### HTTP Client:
```bash
python3 http_client.py --server http://localhost:5000 --size 50 --requests 10
```
- `--server`: Server URL (default: http://localhost:5000)
- `--size`: Matrix size NxN (default: 50)
- `--requests`: Number of requests (default: 10)

## Matrix Sizes

Try different sizes to see performance impact:
- **Small**: `--size 10` (quick testing)
- **Medium**: `--size 50` (balanced)
- **Large**: `--size 100` (more computation)
- **Extra Large**: `--size 200` (stress test)

## Expected Results

### gRPC vs HTTP
- gRPC typically shows **20-30% lower latency** due to Protocol Buffers and HTTP/2
- gRPC has smaller payload sizes (binary vs JSON)
- gRPC has lower network overhead

### Single vs Multi-container
- Multi-container enables **parallel request handling**
- Better resource utilization with multiple workers
- Can handle concurrent requests more efficiently

### Example Output
```
Request 1/10: Total time = 0.0523s, Server computation = 0.0489s
Request 2/10: Total time = 0.0512s, Server computation = 0.0478s
...
============================================================
RESULTS SUMMARY
============================================================
Total requests: 10
Matrix size: 50x50
Average total time: 0.0515s
Average server computation time: 0.0482s
Average network overhead: 0.0033s
Total time for all requests: 0.5150s
============================================================
```

## Stopping Services

```bash
# Stop all Docker services
docker-compose -f docker-compose-grpc-single.yml down
docker-compose -f docker-compose-grpc-multi.yml down
docker-compose -f docker-compose-http-single.yml down
docker-compose -f docker-compose-http-multi.yml down
```

## Troubleshooting

1. **Port already in use**: 
   - Check if services are already running
   - Change ports in docker-compose files

2. **Module not found**:
   - Make sure you've run: `pip3 install -r requirements.txt`
   - Regenerate gRPC code: `python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. matrix.proto`

3. **Connection refused**:
   - Ensure servers are running before starting clients
   - Check Docker containers: `docker ps`

## Project Structure

```
assignment1/
├── matrix.proto                      # Protocol Buffer definition
├── grpc_server.py                    # gRPC server
├── grpc_client.py                    # gRPC client
├── http_server.py                    # HTTP/Flask server
├── http_client.py                    # HTTP client
├── requirements.txt                  # Dependencies
├── Dockerfile.grpc                   # gRPC Docker image
├── Dockerfile.http                   # HTTP Docker image
├── docker-compose-*.yml              # Docker configurations
├── benchmark.py                      # Performance testing
├── setup.sh                          # Setup script
└── README.md                         # Documentation
```

## Next Steps

1. Start with local testing (Option 1) to verify everything works
2. Then try Docker deployments (Option 2) 
3. Run benchmarks to compare performance
4. Experiment with different matrix sizes
5. Analyze the performance differences

Good luck with your assignment! 🚀
