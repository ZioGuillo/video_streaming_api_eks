# app.py
from flask import Flask
import random

app = Flask(__name__)

@app.route('/random')
def get_random_numbers():
    numbers = [random.randint(0, 5) for _ in range(10)]
    response = {
        "data": {"random_number": numbers},
        "message": "success"
    }
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)