from flask import Flask, jsonify
from products.controllers.product_controller import product_controller
from utils import register_service

app = Flask(__name__)

# Registrar el blueprint
app.register_blueprint(product_controller)

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    # El puerto 5002 será para productos
    register_service('products', 5002)
    app.run(host='0.0.0.0', port=5002, debug=True)
