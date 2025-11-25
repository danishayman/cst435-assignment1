#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Matrix Services - All Architectures Test${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Test configuration
MATRIX_SIZE=100
NUM_REQUESTS=10

# Ensure virtual environment is activated
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. matrix.proto
else
    source venv/bin/activate
fi

# Stop all containers first
echo -e "${YELLOW}Stopping all existing containers...${NC}"
docker-compose -f docker-compose-grpc-single.yml down 2>/dev/null
docker-compose -f docker-compose-http-single.yml down 2>/dev/null
docker-compose -f docker-compose-grpc-microservices.yml down 2>/dev/null
docker-compose -f docker-compose-http-microservices.yml down 2>/dev/null
sleep 2

# Results storage
RESULTS_FILE="test_results_$(date +%Y%m%d_%H%M%S).txt"
echo "Test Results - $(date)" > $RESULTS_FILE
echo "Matrix Size: ${MATRIX_SIZE}x${MATRIX_SIZE}" >> $RESULTS_FILE
echo "Requests per test: ${NUM_REQUESTS}" >> $RESULTS_FILE
echo "========================================" >> $RESULTS_FILE
echo "" >> $RESULTS_FILE

# ============================================
# ARCHITECTURE 1: gRPC Single Container
# ============================================
echo -e "\n${GREEN}=====================================${NC}"
echo -e "${GREEN}Architecture 1: gRPC Single Container${NC}"
echo -e "${GREEN}=====================================${NC}"
echo "Architecture 1: gRPC Single Container" >> $RESULTS_FILE

docker-compose -f docker-compose-grpc-single.yml up --build -d
sleep 5

echo -e "${BLUE}Running test...${NC}"
python3 grpc_client.py --server localhost:50051 --size $MATRIX_SIZE --requests $NUM_REQUESTS | tee -a $RESULTS_FILE

docker-compose -f docker-compose-grpc-single.yml down
sleep 2
echo "" >> $RESULTS_FILE

# ============================================
# ARCHITECTURE 2: HTTP Single Container
# ============================================
echo -e "\n${GREEN}=====================================${NC}"
echo -e "${GREEN}Architecture 2: HTTP Single Container${NC}"
echo -e "${GREEN}=====================================${NC}"
echo "Architecture 2: HTTP Single Container" >> $RESULTS_FILE

docker-compose -f docker-compose-http-single.yml up --build -d
sleep 5

echo -e "${BLUE}Running test...${NC}"
python3 http_client.py --server http://localhost:5001 --size $MATRIX_SIZE --requests $NUM_REQUESTS | tee -a $RESULTS_FILE

docker-compose -f docker-compose-http-single.yml down
sleep 2
echo "" >> $RESULTS_FILE

# ============================================
# ARCHITECTURE 3: gRPC Microservices
# ============================================
echo -e "\n${GREEN}=====================================${NC}"
echo -e "${GREEN}Architecture 3: gRPC Microservices${NC}"
echo -e "${GREEN}(3 separate containers)${NC}"
echo -e "${GREEN}=====================================${NC}"
echo "Architecture 3: gRPC Microservices (3 containers)" >> $RESULTS_FILE

docker-compose -f docker-compose-grpc-microservices.yml up --build -d
sleep 5

echo -e "${BLUE}Running test...${NC}"
python3 grpc_client_microservices.py --size $MATRIX_SIZE --requests $NUM_REQUESTS | tee -a $RESULTS_FILE

docker-compose -f docker-compose-grpc-microservices.yml down
sleep 2
echo "" >> $RESULTS_FILE

# ============================================
# ARCHITECTURE 4: HTTP Microservices
# ============================================
echo -e "\n${GREEN}=====================================${NC}"
echo -e "${GREEN}Architecture 4: HTTP Microservices${NC}"
echo -e "${GREEN}(3 separate containers)${NC}"
echo -e "${GREEN}=====================================${NC}"
echo "Architecture 4: HTTP Microservices (3 containers)" >> $RESULTS_FILE

docker-compose -f docker-compose-http-microservices.yml up --build -d
sleep 5

echo -e "${BLUE}Running test...${NC}"
python3 http_client_microservices.py --size $MATRIX_SIZE --requests $NUM_REQUESTS | tee -a $RESULTS_FILE

docker-compose -f docker-compose-http-microservices.yml down
sleep 2
echo "" >> $RESULTS_FILE

# ============================================
# SUMMARY
# ============================================
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}ALL TESTS COMPLETED!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "${YELLOW}Results saved to: ${RESULTS_FILE}${NC}"

echo "" >> $RESULTS_FILE
echo "========================================" >> $RESULTS_FILE
echo "All tests completed successfully!" >> $RESULTS_FILE
echo "========================================" >> $RESULTS_FILE

# Extract and display summary
echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}PERFORMANCE SUMMARY${NC}"
echo -e "${BLUE}========================================${NC}"

echo -e "\n${YELLOW}Extracting key metrics...${NC}"
grep -A 15 "GRAND TOTAL TIME" $RESULTS_FILE | grep -E "Architecture|GRAND TOTAL TIME"

echo -e "\n${GREEN}Full results available in: ${RESULTS_FILE}${NC}"
echo -e "${GREEN}Test completed at: $(date)${NC}"
