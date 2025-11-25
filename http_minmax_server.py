from flask import Flask, request, jsonify
import numpy as np
import time
import argparse

app = Flask(__name__)


@app.route('/minmax', methods=['POST'])
def minmax():
    """Handle matrix min/max calculation request."""
    start_time = time.time()
    
    data = request.json
    
    # Convert to numpy arrays
    matrix_a = np.array(data['matrix_a'])
    matrix_b = np.array(data['matrix_b'])
    
    # Find min and max values
    min_a = float(np.min(matrix_a))
    max_a = float(np.max(matrix_a))
    min_b = float(np.min(matrix_b))
    max_b = float(np.max(matrix_b))
    
    computation_time = time.time() - start_time
    
    # Return result
    return jsonify({
        'min_a': min_a,
        'max_a': max_a,
        'min_b': min_b,
        'max_b': max_b,
        'computation_time': computation_time
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'minmax'})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HTTP Matrix MinMax Server')
    parser.add_argument('--port', type=int, default=5003, help='Server port')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Server host')
    args = parser.parse_args()
    
    print(f"MinMax Service - HTTP Server starting on {args.host}:{args.port}")
    app.run(host=args.host, port=args.port, threaded=True)
