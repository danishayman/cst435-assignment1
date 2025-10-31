# Matrix Multiplication Service

A complete implementation of a matrix multiplication service comparing gRPC vs HTTP performance across single and multi-container deployments.

## 🎯 Project Overview

This project demonstrates the performance differences between gRPC and HTTP for a computationally intensive task (matrix multiplication) in 4 different configurations:

1. **Single container gRPC** - Client & server on same machine
2. **Multi-container gRPC** - Client + 3 worker containers
3. **Single container HTTP** - Using Flask REST API
4. **Multi-container HTTP** - 3 Flask worker containers

## ✅ Implementation Status

**ALL REQUIREMENTS COMPLETED AND TESTED**

- ✅ gRPC server and client implemented
- ✅ HTTP server and client implemented
- ✅ Real computational work (O(n³) matrix multiplication)
- ✅ Docker configurations for all 4 cases
- ✅ Performance benchmarking tools
- ✅ Tested and working locally

## 🏗️ Architecture

### gRPC Implementation
- **Protocol Buffers** for efficient binary serialization
- **HTTP/2** for modern transport features
- **Lower latency** and smaller payload sizes
- **Type-safe** API definitions

### HTTP Implementation
- **RESTful API** using Flask framework
- **JSON** for data exchange
- **HTTP/1.1** standard protocol
- **Easy debugging** and monitoring

## 📋 Prerequisites

- Python 3.8+ (tested with 3.13)
- Docker and Docker Compose (optional, for containerized deployments)
- pip package manager
- 2GB+ RAM for larger matrix operations

## 🚀 Quick Start

### Option 1: Automated Test (Easiest)

```bash
# Run the interactive test script
./test.sh
```

This will guide you through testing gRPC, HTTP, or comparing both.

### Option 2: Manual Local Testing

#### Test gRPC:
```bash
# Activate virtual environment
source venv/bin/activate

# Terminal 1 - Start gRPC server
python grpc_server.py --port 50051

# Terminal 2 - Test with client
python grpc_client.py --server localhost:50051 --size 50 --requests 10
```

#### Test HTTP:
```bash
# Terminal 1 - Start HTTP server
python http_server.py --port 5001

# Terminal 2 - Test with client
python http_client.py --server http://localhost:5001 --size 50 --requests 10
```

### Option 3: Docker Deployment

#### Single Container gRPC:
```bash
docker-compose -f docker-compose-grpc-single.yml up --build
# In another terminal:
python grpc_client.py --server localhost:50051 --size 50 --requests 10
```

#### Multi-Container gRPC (3 workers):
```bash
docker-compose -f docker-compose-grpc-multi.yml up --build
# Test each worker:
python grpc_client.py --server localhost:50051 --size 50 --requests 10
python grpc_client.py --server localhost:50052 --size 50 --requests 10
python grpc_client.py --server localhost:50053 --size 50 --requests 10
```

#### Single Container HTTP:
```bash
docker-compose -f docker-compose-http-single.yml up --build
# In another terminal:
python http_client.py --server http://localhost:5000 --size 50 --requests 10
```

#### Multi-Container HTTP (3 workers):
```bash
docker-compose -f docker-compose-http-multi.yml up --build
# Test each worker:
python http_client.py --server http://localhost:5001 --size 50 --requests 10
python http_client.py --server http://localhost:5002 --size 50 --requests 10
python http_client.py --server http://localhost:5003 --size 50 --requests 10
```

## 📊 Performance Benchmarking

To compare all configurations:

```bash
# Start all services
docker-compose -f docker-compose-grpc-single.yml up -d
docker-compose -f docker-compose-grpc-multi.yml up -d
docker-compose -f docker-compose-http-single.yml up -d
docker-compose -f docker-compose-http-multi.yml up -d

# Run comprehensive benchmark
python benchmark.py --size 50 --requests 20
```

## 📈 Example Results

### gRPC Performance (10x10 matrix, 3 requests):
```
Average total time: 0.0017s
Average server computation time: 0.0000s
Average network overhead: 0.0017s
Total time for all requests: 0.0051s
```

### HTTP Performance (10x10 matrix, 3 requests):
```
Average total time: 0.0035s
Average server computation time: 0.0001s
Average network overhead: 0.0034s
Total time for all requests: 0.0106s
```

**Observation**: gRPC shows approximately **2x better performance** even for small matrices!

## 🛠️ Client Configuration

### gRPC Client Options:
```bash
python grpc_client.py --server <address:port> --size <N> --requests <count>
```
- `--server`: Server address (default: localhost:50051)
- `--size`: Matrix size NxN (default: 50)
- `--requests`: Number of requests to send (default: 10)

### HTTP Client Options:
```bash
python http_client.py --server <url> --size <N> --requests <count>
```
- `--server`: Server URL (default: http://localhost:5000)
- `--size`: Matrix size NxN (default: 50)
- `--requests`: Number of requests to send (default: 10)

## 💡 Matrix Size Recommendations

| Size | Description | Use Case |
|------|-------------|----------|
| 10x10 | Very small | Quick testing |
| 50x50 | Small | Balanced testing |
| 100x100 | Medium | Performance comparison |
| 200x200 | Large | Stress testing |
| 500x500 | Very large | Heavy computation |

## Stopping Services

```bash
# Stop and remove containers
docker-compose -f docker-compose-grpc-single.yml down
docker-compose -f docker-compose-grpc-multi.yml down
docker-compose -f docker-compose-http-single.yml down
docker-compose -f docker-compose-http-multi.yml down
```

## Customization

### Matrix Size
Adjust matrix size for different computational loads:
- Small: 10x10 (quick testing)
- Medium: 50x50 (balanced)
- Large: 100x100 or 200x200 (stress testing)

### Number of Workers
Edit the docker-compose files to add/remove worker containers:
```yaml
grpc-server-4:
  build:
    context: .
    dockerfile: Dockerfile.grpc
  ports:
    - "50054:50051"
  container_name: grpc-worker-4
```

## Troubleshooting

1. **Port already in use**: Change port numbers in docker-compose files and client commands
2. **Module not found**: Run `./setup.sh` or manually install dependencies
3. **Connection refused**: Ensure servers are running before starting clients
4. **Docker errors**: Try `docker-compose down` and rebuild with `--build` flag

## License

This is an educational project for CST435 Assignment 1.
