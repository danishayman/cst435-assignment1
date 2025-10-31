#!/bin/bash

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}Multi-Container Parallel Performance Demo${NC}"
echo -e "${BLUE}============================================${NC}\n"

# Check if Docker services are running
echo -e "${YELLOW}Checking if services are running...${NC}"
if ! docker ps | grep -q "grpc-worker"; then
    echo -e "${RED}gRPC workers not running!${NC}"
    echo -e "${YELLOW}Starting gRPC multi-container setup...${NC}"
    docker-compose -f docker-compose-grpc-multi.yml up -d
    echo -e "${GREEN}Waiting 5 seconds for services to start...${NC}"
    sleep 5
fi

# Activate virtual environment
source venv/bin/activate

MATRIX_SIZE=100
REQUESTS_PER_WORKER=2
TOTAL_REQUESTS=6

echo -e "\n${GREEN}Test Configuration:${NC}"
echo -e "  Matrix Size: ${MATRIX_SIZE}x${MATRIX_SIZE}"
echo -e "  Total Requests: ${TOTAL_REQUESTS}"
echo -e "  Requests per worker (parallel test): ${REQUESTS_PER_WORKER}"
echo -e ""

# Test 1: Single Container (Sequential)
echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}TEST 1: Single Container (Sequential)${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "${YELLOW}All ${TOTAL_REQUESTS} requests handled by ONE worker sequentially${NC}\n"

echo -e "Starting test..."
START_TIME=$(date +%s.%N)
python grpc_client.py --server localhost:50051 --size $MATRIX_SIZE --requests $TOTAL_REQUESTS > /tmp/single_result.txt 2>&1
END_TIME=$(date +%s.%N)
SINGLE_TIME=$(echo "$END_TIME - $START_TIME" | bc)

echo -e "${GREEN}Completed!${NC}"
tail -n 10 /tmp/single_result.txt
echo -e "${GREEN}Total Wall-Clock Time: ${SINGLE_TIME} seconds${NC}"

# Test 2: Multi-Container (Parallel)
echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}TEST 2: Multi-Container (Parallel)${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "${YELLOW}${TOTAL_REQUESTS} requests split across 3 workers IN PARALLEL${NC}\n"

echo -e "Starting parallel test..."
START_TIME=$(date +%s.%N)

# Launch 3 clients in parallel
python grpc_client.py --server localhost:50051 --size $MATRIX_SIZE --requests $REQUESTS_PER_WORKER > /tmp/worker1.txt 2>&1 &
PID1=$!
python grpc_client.py --server localhost:50052 --size $MATRIX_SIZE --requests $REQUESTS_PER_WORKER > /tmp/worker2.txt 2>&1 &
PID2=$!
python grpc_client.py --server localhost:50053 --size $MATRIX_SIZE --requests $REQUESTS_PER_WORKER > /tmp/worker3.txt 2>&1 &
PID3=$!

# Wait for all to complete
wait $PID1
wait $PID2
wait $PID3

END_TIME=$(date +%s.%N)
PARALLEL_TIME=$(echo "$END_TIME - $START_TIME" | bc)

echo -e "${GREEN}Completed!${NC}\n"
echo -e "${YELLOW}Worker 1 (port 50051):${NC}"
tail -n 5 /tmp/worker1.txt
echo -e "\n${YELLOW}Worker 2 (port 50052):${NC}"
tail -n 5 /tmp/worker2.txt
echo -e "\n${YELLOW}Worker 3 (port 50053):${NC}"
tail -n 5 /tmp/worker3.txt

echo -e "\n${GREEN}Total Wall-Clock Time: ${PARALLEL_TIME} seconds${NC}"

# Calculate speedup
SPEEDUP=$(echo "scale=2; $SINGLE_TIME / $PARALLEL_TIME" | bc)

# Final Summary
echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}PERFORMANCE COMPARISON${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "${YELLOW}Single Container (Sequential):${NC}  ${SINGLE_TIME} seconds"
echo -e "${YELLOW}Multi-Container (Parallel):${NC}     ${PARALLEL_TIME} seconds"
echo -e "${GREEN}Speedup:${NC}                        ${SPEEDUP}x faster!"
echo -e "${BLUE}========================================${NC}\n"

if (( $(echo "$SPEEDUP > 2.0" | bc -l) )); then
    echo -e "${GREEN}✓ Excellent! Multi-container setup shows significant speedup!${NC}"
    echo -e "${GREEN}✓ This demonstrates the power of parallel processing!${NC}"
elif (( $(echo "$SPEEDUP > 1.5" | bc -l) )); then
    echo -e "${YELLOW}✓ Good speedup observed. Network overhead reduces perfect scaling.${NC}"
else
    echo -e "${RED}⚠ Lower than expected speedup. This could be due to:${NC}"
    echo -e "${RED}  - Small matrix size (less computation)${NC}"
    echo -e "${RED}  - Network overhead${NC}"
    echo -e "${RED}  - System load${NC}"
fi

echo -e "\n${BLUE}Key Insight:${NC}"
echo -e "The multi-container setup processes ${TOTAL_REQUESTS} requests"
echo -e "in roughly the time it takes to process ${REQUESTS_PER_WORKER} requests sequentially"
echo -e "because the 3 workers operate IN PARALLEL!\n"
