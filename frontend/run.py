from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
import requests
from utils import register_service
import os

app = Flask(__name__, template_folder='web/templates', static_folder='web/static')
app.secret_key = 'secret123'
CORS(app, supports_credentials=True)

# Obtener URLs de los servicios desde variables de entorno
USERS_API_URL = os.environ.get('USERS_API_URL')
PRODUCTS_API_URL = os.environ.get('PRODUCTS_API_URL')
ORDERS_API_URL = os.environ.get('ORDERS_API_URL')

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

# --- Rutas para renderizar las páginas HTML ---

@app.route('/')
def index():
    return render_template('index.html') # Página de Login

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/my-orders')
def my_orders():
    return render_template('my_orders.html')

# --- Rutas de Proxy a los Microservicios ---

# Proxy para USUARIOS
@app.route('/api/users/register', methods=['POST'])
def register_user():
    response = requests.post(f"{USERS_API_URL}/api/users/register", json=request.get_json())
    return jsonify(response.json()), response.status_code

@app.route('/api/users/login', methods=['POST'])
def login_user():
    response = requests.post(f"{USERS_API_URL}/api/users/login", json=request.get_json())
    return jsonify(response.json()), response.status_code

# Proxy para PRODUCTOS
@app.route('/api/products', methods=['GET'])
def get_products():
    response = requests.get(f"{PRODUCTS_API_URL}/api/products")
    return jsonify(response.json()), response.status_code

# Proxy para ÓRDENES
@app.route('/api/orders', methods=['POST'])
def create_order():
    response = requests.post(f"{ORDERS_API_URL}/api/orders", json=request.get_json())
    return jsonify(response.json()), response.status_code
    
@app.route('/api/orders/user/<username>', methods=['GET'])
def get_orders_by_user(username):
    # Nota: Este endpoint debe ser implementado en el microservicio de órdenes
    response = requests.get(f"{ORDERS_API_URL}/api/orders/user/{username}")
    return jsonify(response.json()), response.status_code


if __name__ == '__main__':
    register_service('frontend', 5000)
    app.run(host='0.0.0.0', port=5000, debug=True)
