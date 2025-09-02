from flask import Flask, jsonify
from orders.controllers.order_controller import order_controller
from utils import register_service

app = Flask(__name__)
app.register_blueprint(order_controller)

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    # El puerto 5003 será para órdenes
    register_service('orders', 5003)
    app.run(host='0.0.0.0', port=5003, debug=True)
