#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Matrix Multiplication Service Test Suite${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. matrix.proto
else
    source venv/bin/activate
fi

# Function to test gRPC
test_grpc() {
    echo -e "\n${GREEN}Testing gRPC Implementation${NC}"
    echo -e "${BLUE}Starting gRPC server on port 50051...${NC}"
    python grpc_server.py --port 50051 &
    SERVER_PID=$!
    sleep 2
    
    echo -e "${BLUE}Running gRPC client (10x10 matrix, 5 requests)...${NC}"
    python grpc_client.py --server localhost:50051 --size 10 --requests 5
    
    echo -e "${BLUE}Stopping gRPC server...${NC}"
    kill $SERVER_PID
}

# Function to test HTTP
test_http() {
    echo -e "\n${GREEN}Testing HTTP Implementation${NC}"
    echo -e "${BLUE}Starting HTTP server on port 5001...${NC}"
    python http_server.py --port 5001 &
    SERVER_PID=$!
    sleep 2
    
    echo -e "${BLUE}Running HTTP client (10x10 matrix, 5 requests)...${NC}"
    python http_client.py --server http://localhost:5001 --size 10 --requests 5
    
    echo -e "${BLUE}Stopping HTTP server...${NC}"
    kill $SERVER_PID
}

# Function to compare performance
compare_performance() {
    echo -e "\n${GREEN}Performance Comparison${NC}"
    
    # gRPC Test
    echo -e "${BLUE}Testing gRPC (50x50 matrix, 10 requests)...${NC}"
    python grpc_server.py --port 50051 &
    GRPC_PID=$!
    sleep 2
    python grpc_client.py --server localhost:50051 --size 50 --requests 10 > /tmp/grpc_result.txt
    kill $GRPC_PID
    
    # HTTP Test
    echo -e "${BLUE}Testing HTTP (50x50 matrix, 10 requests)...${NC}"
    python http_server.py --port 5001 &
    HTTP_PID=$!
    sleep 2
    python http_client.py --server http://localhost:5001 --size 50 --requests 10 > /tmp/http_result.txt
    kill $HTTP_PID
    
    echo -e "\n${GREEN}Results:${NC}"
    echo -e "${BLUE}gRPC Results:${NC}"
    cat /tmp/grpc_result.txt
    echo -e "\n${BLUE}HTTP Results:${NC}"
    cat /tmp/http_result.txt
}

# Main menu
echo -e "Select test option:"
echo -e "1) Test gRPC only"
echo -e "2) Test HTTP only"
echo -e "3) Compare gRPC vs HTTP performance"
echo -e "4) Run all tests"
echo -e "5) Exit"
echo -e -n "\n${YELLOW}Enter choice [1-5]: ${NC}"

read choice

case $choice in
    1)
        test_grpc
        ;;
    2)
        test_http
        ;;
    3)
        compare_performance
        ;;
    4)
        test_grpc
        test_http
        compare_performance
        ;;
    5)
        echo -e "${BLUE}Exiting...${NC}"
        exit 0
        ;;
    *)
        echo -e "${YELLOW}Invalid option${NC}"
        exit 1
        ;;
esac

echo -e "\n${GREEN}Testing complete!${NC}"
